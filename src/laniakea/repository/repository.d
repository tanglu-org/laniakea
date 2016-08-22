/*
 * Copyright (C) 2016 Matthias Klumpp <matthias@tenstral.net>
 *
 * Licensed under the GNU Lesser General Public License Version 3
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the license, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

module laniakea.repository.repository;

import std.stdio;
import std.path : buildPath, dirName;
import std.string : strip, format;
import std.array : appender, split, empty;
import std.conv : to;
static import std.file;

import requests : getContent;

import laniakea.logging;
import laniakea.config : Config;
import laniakea.utils : isRemote, splitStrip;
import laniakea.tagfile;
import laniakea.packages;


/**
 * Allows reading data from a Debian repository.
 */
class Repository
{

private:
    string rootDir;
    string repoUrl;

public:

    this (string location, string repoName = null)
    {
        if (isRemote (location)) {
            auto conf = Config.get ();
            rootDir = buildPath (conf.cacheDir, "repos_tmp", repoName);
            std.file.mkdirRecurse (rootDir);
            repoUrl = location;
        } else {
            rootDir = location;
            repoUrl = null;
        }
    }

    /**
     * Download a file and retrieve a filename.
     */
    string getRepoFile (const string repoLocation)
    {
        if (repoUrl is null) {
            immutable fname = buildPath (rootDir, repoLocation);
            if (std.file.exists (fname))
                return fname;
        } else {
            immutable sourceUrl = buildPath (repoUrl, repoLocation);
            immutable targetFname = buildPath (rootDir, repoLocation);
            std.file.mkdirRecurse (targetFname.dirName);

            auto content = getContent (sourceUrl);
            auto f = File (targetFname, "wb");
            f.rawWrite (content.data);
            f.close ();

            return targetFname;
        }

        // There was an error, we couldn't find or download the file
        logError ("Could not find repository file '%s'", repoLocation);
        return null;
    }

    @property @safe
    string baseDir () { return rootDir; }

    SourcePackage[] getSourcePackages (const string suite, const string component)
    {
        immutable indexFname = getRepoFile (buildPath ("dists", suite, component, "source", "Sources.xz"));
        if (indexFname.empty)
            return [];

        auto tf = new TagFile;
        tf.open (indexFname);

        auto pkgs = appender!(SourcePackage[]);
        do {
            auto pkgname = tf.readField ("Package");
            if (!pkgname)
                continue;

            SourcePackage pkg;
            pkg.name = pkgname;

            pkg.ver = tf.readField ("Version");
            pkg.architectures = tf.readField ("Architecture").split (" ");
            pkg.standardsVersion = tf.readField ("Standards-Version");
            pkg.format = tf.readField ("Format");

            pkg.vcsBrowser = tf.readField ("Vcs-Browser");
            pkg.homepage = tf.readField ("Homepage");
            pkg.maintainer = tf.readField ("Maintainer");
            pkg.uploaders = tf.readField ("Uploaders", "").splitStrip (","); // FIXME: Careful! Splitting just by comma isn't enough!

            pkg.buildDepends = tf.readField ("Build-Depends", "").splitStrip (",");
            pkg.directory = tf.readField ("Directory");

            auto files = appender!(ArchiveFile[]);
            immutable filesRaw = tf.readField ("Checksums-Sha256"); // f43923ace1c558ad9f9fa88eb3f1764a8c0379013aafbc682a35769449fe8955 2455 0ad_0.0.20-1.dsc
            foreach (ref fileRaw; filesRaw.split ('\n')) {
                auto parts = fileRaw.strip.split (" ");
                if (parts.length != 3)
                    continue;

                ArchiveFile file;
                file.sha256sum = parts[0];
                file.size = to!size_t (parts[1]);
                file.fname = parts[2];

                files ~= file;
            }
            pkg.files = files.data;

            immutable rawPkgList = tf.readField ("Package-List");
            if (rawPkgList is null) {
                foreach (bin; tf.readField ("Binary", "").splitStrip (",")) {
                    PackageInfo pi;
                    pi.type = DebType.DEB;
                    pi.name = bin;
                    pi.ver = pkg.ver;
                    pkg.binaries ~= pi;
                }
            } else {
                pkg.binaries = parsePackageListString (rawPkgList, pkg.ver);
            }

            // Do some issue-reporting
            if (pkg.files.empty)
                logWarning ("Source package %s/%s seems to have no files.", pkg.name, pkg.ver);

            pkgs ~= pkg;
        } while (tf.nextSection ());

        return pkgs.data;
    }

    BinaryPackage[] getBinaryPackages (const string suite, const string component, const string arch)
    {
        immutable indexFname = getRepoFile (buildPath ("dists", suite, component, "binary-%s".format (arch), "Packages.xz"));
        if (indexFname.empty)
            return [];

        auto tf = new TagFile;
        tf.open (indexFname);

        auto pkgs = appender!(BinaryPackage[]);
        do {
            auto pkgname = tf.readField ("Package");
            if (!pkgname)
                continue;

            BinaryPackage pkg;
            pkg.name = pkgname;

            pkg.ver = tf.readField ("Version");
            pkg.architecture = tf.readField ("Architecture");
            pkg.installedSize = to!size_t (tf.readField ("Installed-Size"));
            pkg.maintainer = tf.readField ("Maintainer");

            pkg.depends = tf.readField ("Depends", "").splitStrip (",");
            pkg.preDepends = tf.readField ("Pre-Depends", "").splitStrip (",");

            pkg.homepage = tf.readField ("Homepage");
            pkg.section = tf.readField ("Section");

            pkg.priority = packagePriorityFromString (tf.readField ("Priority"));

            pkg.file.fname = tf.readField ("Filename");
            pkg.file.size = to!size_t (tf.readField ("Size"));
            pkg.file.sha256sum = tf.readField ("SHA256");

            // Do some issue-reporting
            if (pkg.file.fname.empty)
                logWarning ("Binary package %s/%s seems to have no files.", pkg.name, pkg.ver);

            pkgs ~= pkg;
        } while (tf.nextSection ());

        return pkgs.data;
    }

}

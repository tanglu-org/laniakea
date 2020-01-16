# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Matthias Klumpp <matthias@tenstral.net>
#
# Licensed under the GNU Lesser General Public License Version 3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the license, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.


__all__ = ['message_templates']


def green(m):
    return '<font color="#27ae60">{}</font>'.format(m)


def orange(m):
    return '<font color="#f39c1f">{}</font>'.format(m)


def red(m):
    return '<font color="#da4453">{}</font>'.format(m)


#
# Templates for jobs
#

templates_jobs = \
    {'_lk.jobs.job-assigned':
     '''Assigned {job_kind} job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a> on architecture <code>{job_architecture}</code> to <em>{client_name}</em>''',

     '_lk.jobs.job-accepted':
     'Job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a> was ' + green('accepted') + ' by <em>{client_name}</em>',

     '_lk.jobs.job-rejected':
     'Job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a> was ' + red('rejected') + ' by <em>{client_name}</em>',

     '_lk.jobs.job-finished':
     '''Job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a> finished with result <em>{result}</em>''',
     }

#
# Templates for Synchrotron
#


def pretty_package_imported(tag, data):
    info = 'package <b>{name}</b> from {src_os} <em>{suite_src}</em> → <em>{suite_dest}</em>, new version is <code>{version}</code>.'.format(**data)
    if data.get('forced'):
        return 'Enforced import of ' + info
    else:
        return 'Imported package ' + info


templates_synchrotron = \
    {'_lk.synchrotron.src-package-imported': pretty_package_imported,

     '_lk.synchrotron.new-autosync-issue':
     ('New automatic synchronization issue for ' + red('<b>{name}</b>') + ' from {src_os} <em>{suite_src}</em> → <em>{suite_dest}</em> '
      '(source: <code>{version_src}</code>, destination: <code>{version_dest}</code>). Type: {kind}'),

     '_lk.synchrotron.resolved-autosync-issue':
     'The <em>{kind}</em> synchronization issue for <b>{name}</b> from {src_os} <em>{suite_src}</em> → <em>{suite_dest}</em> was ' + green('resolved') + '.'
     }


#
# Templates for Rubicon
#


def pretty_upload_accepted(tag, data):
    if data.get('job_failed'):
        tmpl = 'Accepted upload for ' + red('failed') + ' job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a>.'
    else:
        tmpl = 'Accepted upload for ' + green('successful') + ' job <a href="{url_webview}/jobs/job/{job_id}">{job_id:11.11}</a>.'
    return tmpl.format(**data)


templates_rubicon = \
    {'_lk.rubicon.upload-accepted': pretty_upload_accepted,

     '_lk.rubicon.upload-rejected':
     '<b>Rejected</b> upload <code>{dud_filename}</code>. Reason: <code>{reason}</code>'
     }


#
# Templates for Isotope
#


templates_isotope = \
    {'_lk.isotope.recipe-created':
     'Created new <code>{kind}</code> image build recipe <code>{name}</code> for {distribution} <b>{suite}</b> of flavor <b>{flavor}</b> on <code>{architectures}</code>',

     '_lk.isotope.build-job-added':
     ('Created <code>{kind}</code> image build job on <code>{architecture}</code> for {distribution} <b>{suite}</b> of flavor <b>{flavor}</b>. '
      '| <a href="{url_webview}/jobs/job/{job_id}">\N{CIRCLED INFORMATION SOURCE}</a>'),

     '_lk.isotope.image-build-failed':
     ('A <code>{kind}</code> image for {distribution} ' + red('failed') + ' to build for <b>{suite}</b>, flavor <b>{flavor}</b> on <code>{architecture}</code>. '
      '| <a href="{url_webview}/jobs/job/{job_id}">\N{CIRCLED INFORMATION SOURCE}</a>'),

     '_lk.isotope.image-build-success':
     ('A <code>{kind}</code> image for {distribution} was built ' + green('successfully') + ' for <b>{suite}</b>, flavor <b>{flavor}</b> on <code>{architecture}</code>. '
      'The image has been ' + green('published') + ' for download. | <a href="{url_webview}/jobs/job/{job_id}">\N{CIRCLED INFORMATION SOURCE}</a>')

     }


#
# Templates for the Archive
#


def pretty_source_package_published(tag, data):
    data['suites_str'] = ', '.join(data['suites'])

    tmpl = 'Source package <b>{name}</b> <b><em>{version}</em></b> ({component}) was ' + green('published') + ' in the archive, available in suites <em>{suites_str}</em>.'
    if data['suites']:
        tmpl = tmpl + ' | <a href="{url_webview}/export/changelogs/{component}/{name:1.1}/{name}/' + data['suites'][0] + '_changelog">\N{DOCUMENT}</a>'

    return tmpl.format(**data)


templates_archive = \
    {'_lk.archive.package-build-success':
     ('Package build for <b>{pkgname}</b> <b><em>{version}</em></b> on <code>{architecture}</code> in <em>{suite}</em> was ' + green('successful') + '. '
      '| <a href="{url_webswview}/package/builds/job/{job_id}">\N{CIRCLED INFORMATION SOURCE}</a>'),

     '_lk.archive.package-build-failed':
     ('Package build for <b>{pkgname}</b> <b><em>{version}</em></b> on <code>{architecture}</code> in <em>{suite}</em> has ' + red('failed') + '. '
      '| <a href="{url_webswview}/package/builds/job/{job_id}">\N{CIRCLED INFORMATION SOURCE}</a>'),

     '_lk.archive.source-package-published': pretty_source_package_published,

     '_lk.archive.source-package-published-in-suite':
     'Source package <b>{name}</b> <b><em>{version}</b></em> was ' + green('added') + ' to suite <em>{suite_new} ({component})</em>.',

     '_lk.archive.source-package-suite-removed':
     'Source package <b>{name}</b> <b><em>{version}</b></em> was ' + red('removed') + ' from suite <em>{suite_old} ({component})</em>.',

     '_lk.archive.removed-source-package':
     'Package <b>{name}</b> <b><em>{version}</b></em> ({component}) was ' + orange('removed') + ' from the archive.'
     }


#
# Templates for Spears
#


def pretty_excuse_change(tag, data):
    removal = False
    if data.get('version_new') == '-':
        data['version_new'] = '(' + red('removal') + ')'
        removal = True

    if tag == '_lk.spears.new-excuse':
        if data.get('version_old') == '-':
            old_ver_info = 'Package is ' + green('new') + ' to target!'
        else:
            old_ver_info = 'Version in target is: {version_old}'

        tmpl = ('Package <b>{source_package}</b> {version_new} was ' + red('blocked') + ' from its <em>{suite_source}</em> → <em>{suite_target}</em> '
                'migration. ' + old_ver_info + ' | <a href="{url_webview}/migrations/excuse/{uuid}">\N{CIRCLED INFORMATION SOURCE}</a>')

    elif tag == '_lk.spears.excuse-removed':
        tmpl = 'Migration excuse for package <b>{source_package}</b> <b><em>{version_new}</em></b> was ' + green('invalidated') + '.'
        if removal:
            tmpl = tmpl + ' The package is now deleted from <em>{suite_target}</em>. Previous version was: <code>{version_old}</code>'
        else:
            if data.get('version_old') == '-':
                old_ver_info = 'This package is ' + green('new') + ' in <em>{suite_target}</em>.'
            else:
                old_ver_info = 'Previous version in target was: <code>{version_old}</code>'

            tmpl = tmpl + ' The package migrated from <em>{suite_source}</em> → <em>{suite_target}</em>. ' + old_ver_info

    return tmpl.format(**data)


templates_spears = \
    {'_lk.spears.new-excuse': pretty_excuse_change,
     '_lk.spears.excuse-removed': pretty_excuse_change
     }


#
# Assemble complete template set
#
message_templates = {}
message_templates.update(templates_jobs)
message_templates.update(templates_synchrotron)
message_templates.update(templates_rubicon)
message_templates.update(templates_isotope)
message_templates.update(templates_archive)
message_templates.update(templates_spears)

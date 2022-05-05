import logging
import tarfile
import os.path
from xml.dom import minidom

from django.conf import settings

logger = logging.getLogger()

def write_vertical(output_dir_path, conf, vert_display_name):
    """
    Writes verticals in file in xml format
    Inputs:
        output_dir_path: Path to root of output.
        conf: configuration data.
        vert_display_name: vertical display name.
    """
    doc = minidom.Document()
    elem_vertical = doc.createElement('vertical')
    elem_vertical.setAttribute('display_name', vert_display_name)
    doc.appendChild(elem_vertical)

    # Create lti component for xml
    elem_lti = doc.createElement('lti_advantage_consumer')
    elem_lti.setAttribute('url_name', conf.get('url_name'))
    elem_lti.setAttribute('xblock-family', conf.get('xblock-family'))
    elem_lti.setAttribute('has_score', conf.get('has_score'))
    elem_lti.setAttribute(
        'ask_to_send_username',
        conf.get('ask_to_send_username')
    )
    elem_lti.setAttribute('ask_to_send_name', conf.get('ask_to_send_name'))
    elem_lti.setAttribute('ask_to_send_email', conf.get('ask_to_send_email'))
    elem_lti.setAttribute('tool_id', conf.get('tool_id'))
    elem_lti.setAttribute('launch_url', conf.get('launch_url'))
    elem_lti.setAttribute('custom_parameters', conf.get('custom_parameters'))
    elem_vertical.appendChild(elem_lti)

    doc_str = doc.toprettyxml()

    with open(str(output_dir_path), 'w', encoding='utf-8') as vert_file:
        vert_file.write(doc_str)

    return True


def compress_course(source_dir, course_key_tags):
    """
    Compresses course into gz type.
    Inputs:
        source_dir: dir to be compressed.
        course_key_tags: course url tags.
    """
    output_filename = (settings.ENV_NAME + '_' + course_key_tags['course_org'] + '_' +
                       course_key_tags['course_run'] + '_' +
                       course_key_tags['course_url'] + '.tar.gz')

    with tarfile.open("media/output/" + output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    logger.info(  # pylint: disable=logging-fstring-interpolation
        f"New course file {output_filename} has been created for {settings.ENV_NAME} "
        "environment."
    )

    return "output/" + output_filename

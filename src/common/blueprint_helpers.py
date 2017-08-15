
def bp_template_dir(*filenames):
    # TODO make this smart
    bp_path = '../../templates'
    return '/'.join([bp_path, *filenames])
from .misc import (
        camel_to_underscore,
        convert_date,
        convert_datetime,
        dict_from_dataframe,
        dir_list,
        download_if_new,
        get_ulmo_dir,
        mkdir_if_doesnt_exist,
        module_with_dependency_errors,
        module_with_deprecation_warnings,
        open_file_for_url,
        parse_fwf,
        raise_dependency_error,
        save_pretty_printed_xml,
        to_bytes,
    )

from .raster import (
        extract_from_zip,
        mosaic_and_clip,
        download_tiles,
        generate_raster_uid,
    )

try:
    from .pytables import (
            get_default_h5file_path,
            get_or_create_group,
            get_or_create_table,
            open_h5file,
            update_or_append_sortable,
        )
except ImportError:
    get_default_h5file_path = raise_dependency_error
    get_or_create_group = raise_dependency_error
    get_or_create_table = raise_dependency_error
    open_h5file = raise_dependency_error
    update_or_append_sortable = raise_dependency_error

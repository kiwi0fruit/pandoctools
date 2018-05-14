# Predefined:
# core_config, user_config, in_ext, out_ext, input_file

# ;; jumps to esac
case "${in_ext}" in
    "" | md)
        from=markdown
        ;;
    *)
        from="${in_ext}"
esac

case "${out_ext}" in
    "" | md)
        to=markdown
        ;;
    *)
        to="${out_ext}"
esac

# stdin from previous operations + Meta-Default.yaml:
inputs=("stdin" "${core_config}/Meta-Default.yaml")
reader_args=(-f "${from}")
writer_args=(-t "${to}" --standalone --self-contained)

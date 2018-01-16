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

reader_args=(-f "${from}")
writer_args=(-t "${to}" --standalone --self-contained)
inputs="stdin"
# stdin from previous operations + meta-default.yaml:
all_inputs=("stdin" "${config}/meta-default.yaml")

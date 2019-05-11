runTest() {

    # The first argument is the code we should get
    ERROR="${1:-}"
    shift
    OUTPUT=${1:-}
    shift

    "$@" > "${OUTPUT}" 2>&1
    RETVAL="$?"

    if [ "$ERROR" = "0" -a "$RETVAL" != "0" ]; then
        echo "$@ (retval=$RETVAL) ERROR"
        cat ${OUTPUT}
        echo "Output in ${OUTPUT}"
        exit 1
    elif [ "$ERROR" != "0" -a "$RETVAL" = "0" ]; then
        echo "$@ (retval=$RETVAL) ERROR"
        echo "Output in ${OUTPUT}"
        cat ${OUTPUT}
        exit 1
    else
        echo "$@ (retval=$RETVAL) OK"
    fi
}

$.fn.getFormObject = function() {
    var object = $(this).serializeArray().reduce(function(obj, item) {
        var name = item.name.replace("[]", "");
        if ( typeof obj[name] !== "undefined" ) {
            if ( !Array.isArray(obj[name]) ) {
                obj[name] = [ obj[name], item.value ];
            } else {
               obj[name].push(item.value);
            }
        } else {
            obj[name] = item.value;
        }
        return obj;
    }, {});
    return object;
}
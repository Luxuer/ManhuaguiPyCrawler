getPicUrl: function (n) {
    var r = pVars.manga.filePath + t.files[n] + "?cid=" + t.cid,
        i;
    for (i in t.sl) r += "&" + i + "=" + t.sl[i];
    return r
}
loadIMG: function () {
    var n = this;
    h(function () {
        $("span.nopic,#erroraudit_show").remove(), $("#imgLoading").show(), pVars.curFile = n.getPicUrl(pVars.page - 1), $('<img alt="' + t.bname + " " + t.cname + '" id="mangaFile" src="' + pVars.curFile + '" class="mangaFile" data-tag="mangaFile" style="display:block;" />').load(function () {
            n.success(this)
        }).error(function () {
            n.error(this)
        }).appendTo("#mangaBox"), SMH.utils.imgGrayScale()
    }), $(function () {
        $("#pagination").html(SMH.pager({
            cp: pVars.page - 1,
            pc: t.len
        })), setTimeout(function () {
            SMH.history.add({
                bn: t.bname,
                bid: t.bid,
                cn: t.cname,
                cid: t.cid,
                p: pVars.page,
                t: parseInt(+new Date / 1e3)
            })
        }, 1e3)
    })
}
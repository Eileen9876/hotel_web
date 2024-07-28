$.ajaxSetup({
    async: false,
    contentType: "application/json; charset=utf-8"
});

get_room_data();

get_store_data();

//-------------------- 取得訂房資訊並顯示於網頁上 --------------------//

$("#book_btn_").on('click', () => {
    const data = {
        name: $("#book_name").val(),
        startDate: $("#book_startDate").val(),
        endDate: $("#book_endDate").val(),
        pageIdx: 1
    }

    //取得訂房資訊
    $.post("http://127.0.0.1:8000/get_book_info", JSON.stringify(data), (res) => {
        if (res["status"] == "error") {
            alert("取得訂房資訊失敗\r\n" + res["content"])
            return;
        }

        listData(res["content"]);
    });

    //將資料顯示於網頁上
    function listData(data) {
        if (Object.keys(data).length === 0) {
            $("#book_tbody").html("<tr>無資料</tr>");
            return;
        }

        var htmlContent = "";

        for (var idx in data) {
            data_ = data[idx]

            htmlContent += "<tr>\
                                <td>" + data_["bookId"] + "</td>\
                                <td>" + data_["roomId"] + "</td>\
                                <td>" + data_["name"] + "</td>\
                                <td>" + data_["email"] + "</td>\
                                <td>" + data_["arrDate"] + "</td>\
                                <td>" + data_["depDate"] + "</td>\
                                <td>" + data_["people"] + "</td>\
                            </tr>"
        };

        $("#book_tbody").html(htmlContent);

        htmlContent = '<div class="col-auto"><a href="javascript:pageChange(\'l\');" style="color: #6e6e6e;">&laquo;</a></div>\
                        <div class="col-auto" id="book_table_idx">1</div>\
                        <div class="col-auto"><a href="javascript:pageChange(\'r\');" style="color: #6e6e6e;">&raquo;</a></div>'

        $("#book_page_idx_").html(htmlContent);
    }
});

//表單頁面
function pageChange(dir) {

    //確認是否超出頁數
    var pageIdx;
    if (dir == "l") pageIdx = parseInt($("#book_table_idx").html()) - 1;
    else pageIdx = parseInt($("#book_table_idx").html()) + 1;

    if (pageIdx == 0) return;

    //設置頁碼
    $("#book_table_idx").html(pageIdx);

    const data = {
        name: $("#book_name").val(),
        startDate: $("#book_startDate").val(),
        endDate: $("#book_endDate").val(),
        pageIdx: pageIdx
    }

    //取得訂房資訊
    $.post("http://127.0.0.1:8000/get_book_info", JSON.stringify(data), (res) => {
        if (res["status"] == "error") {
            alert("無法取得訂房資訊\r\n" + res["content"]);
            return;
        }

        listData(res["content"]);
    });

    //將資料顯示於網頁上
    function listData(data) {
        if (Object.keys(data).length === 0) {
            $("#book_tbody").html("<tr>無資料</tr>");
            return;
        }

        var htmlContent = "";

        for (var idx in data) {
            data_ = data[idx]

            htmlContent += "<tr>\
                                <td>" + data_["bookId"] + "</td>\
                                <td>" + data_["roomId"] + "</td>\
                                <td>" + data_["name"] + "</td>\
                                <td>" + data_["email"] + "</td>\
                                <td>" + data_["arrDate"] + "</td>\
                                <td>" + data_["depDate"] + "</td>\
                                <td>" + data_["people"] + "</td>\
                            </tr>"
        };

        $("#book_tbody").html(htmlContent);
    }
}

//-------------------- 取得當天房客資訊並顯示於網頁上 --------------------//

function get_room_data() {
    const date = new Date();

    const data = {
        name: "",
        startDate: date.toISOString().split('T')[0],
        endDate: date.toISOString().split('T')[0],
        pageIdx: 1
    }

    console.log(data)

    //取得訂房資訊
    $.post("http://127.0.0.1:8000/get_book_info", JSON.stringify(data), (res) => {
        if (res["status"] == "error") {
            alert("無法取得訂房資訊\r\n" + res["content"]);
            return;
        }

        listData(res["content"]);
    });


    //將資料顯示於網頁上
    function listData(data) {
        for (var idx in data) {
            data_ = data[idx]

            var htmlContent = $("#room" + data_["roomId"]).html()

            htmlContent += '<div class="row box3">\
                                <div class="col-3">\
                                    <p>訂房編號</p>\
                                    <p>姓名</p>\
                                    <p>Email</p>\
                                    <p>抵達日期</p>\
                                    <p>離開日期</p>\
                                    <p>人數</p>\
                                </div>\
                                <div class="col-6">\
                                    <p>' + data_["bookId"] + '</p>\
                                    <p>' + data_["name"] + '</p>\
                                    <p>' + data_["email"] + '</p>\
                                    <p>' + data_["arrDate"] + '</p>\
                                    <p>' + data_["depDate"] + '</p>\
                                    <p>' + data_["people"] + '</p>\
                                </div>\
                            </div>'
    
            $("#room" + data_["roomId"]).html(htmlContent)
        }
    }
}

//-------------------- 取得商鋪資訊並顯示於網頁上 --------------------//

function get_store_data() {
    const data = {
        colName: ["storeId", "storeName", "info", "image"]
    };

    //取得商鋪資訊
    $.post("http://127.0.0.1:8000/get_store_info/All", JSON.stringify(data), (res) => {
        if (res["status"] == "error") {
            alert("無法取得商鋪資訊\r\n" + res["content"]);
            return;
        }

        listData(res["content"]);
    });

    //在網頁中列出資料
    async function listData(data) {

        var htmlContent = "";

        for (var storeId in data) {
            const data_ = data[storeId];

            htmlContent += '<div class="col-3 store_col_">\
                                <img src="' + data_["image"]["storeImage"] + '">\
                                <h5 class="text-center text-bl font-weight-bold" style="margin-bottom:10px">' + data_["storeName"] + '</h5>\
                                <div class="store_col_info"><p>' + data_["info"] + '</p></div>\
                                <div class="row justify-content-center">\
                                    <a href="/control/storeDetailed?storeId=' + storeId + '" class="btn" id="store_btn_">詳細資訊</a>\
                                </div>\
                            </div>'
        }

        htmlContent += '<div class="col-3" id="addStoreBtn_div">\
                            <a href="/control/addStore" class="btn" id="addStoreBtn"><h4>新增店家</h4></a>\
                        </div>'

        $("#storeInfo_").html(htmlContent);
    }
}


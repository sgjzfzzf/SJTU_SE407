function whenChooseTeacher(id) {
    //选择教师后发送Ajax请求并及时刷新页面
    var course_id = document.getElementById("course_id").innerHTML;
    var teacher = document.getElementById(id).value;
    var httpReq = new XMLHttpRequest();
    var url = '/getteachercoursepage/' + course_id + '/' + teacher;
    httpReq.open('GET', url, true);
    httpReq.send();
    httpReq.onreadystatechange = function () {
        if (httpReq.status == 200 && httpReq.readyState == 4) {
            document.getElementById("comments").innerHTML = httpReq.responseText;
        }
    }
}

function likeComment(id) {
    var like_num = document.getElementById("like_num_" + id);
    var button = document.getElementById("like_" + id);
    var a = document.getElementById("fa_" + id);
    if (button.value == "Like") {
        var httpReq = new XMLHttpRequest();
        var url = '/addLike/' + id;
        httpReq.open('GET', url, true);
        httpReq.send();
        httpReq.onreadystatechange = function () {
            if (httpReq.status == 200 && httpReq.readyState == 4) {
                like_num.innerHTML = httpReq.responseText;
                button.value = "Liked";
                a.className = "fa fa-thumbs-up";
            }
        }
    }
    else if (button.value == "Liked") {
        var httpReq = new XMLHttpRequest();
        var url = '/deleteLike/' + id;
        httpReq.open('GET', url, true);
        httpReq.send();
        httpReq.onreadystatechange = function () {
            if (httpReq.status == 200 && httpReq.readyState == 4) {
                like_num.innerHTML = httpReq.responseText;
                button.value = "Like";
                a.className = "fa fa-thumbs-o-up";
            }
        }
    }
}

function deleteComment(id) {
    var url = '/deletecomment/' + id;
    var httpReq = new XMLHttpRequest();
    httpReq.open('GET', url, true);
    httpReq.send();
    httpReq.onreadystatechange = function () {
        if (httpReq.status == 200 && httpReq.readyState == 4) {
            document.write(httpReq.responseText);
        }
    }
}
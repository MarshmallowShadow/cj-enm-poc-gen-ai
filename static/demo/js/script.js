//로딩 중인지 확인
let loading = false;

const fileTypes = ["text/plain", "application/rtf", "text/markdown", "text/html", "application/xml", "text/csv", "application/json", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.oasis.opendocument.text"];

window.CSRF_TOKEN = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)')?.pop() || '';
$(document).ready(function() {
    let accept = "";
    fileTypes.forEach(type => accept += type + ", ");
    $("#analyzeFile").attr("accept", accept);

    //Range 초기값
    $("#temperatureVal").text($("#temperature").val());
    $("#topPVal").text($("#topP").val());
    $("#presencePenaltyVal").text($("#presencePenalty").val());

    //클라우드 파일 목록 표시
    updateFileList(fileList);

   //파일명, 크기 표시
    $("#analyzeFile").on("change", function(e) {
        let fileName = "";
        if(e.target.files[0]) {
            if(fileTypes.indexOf(e.target.files[0].type) < 0) {
                alert("해석 불가능한 파일 형식입니다.");
                return false;
            }

            let fileSize = getFileSize(e.target.files[0]);
            fileName = e.target.files[0].name + " (" + fileSize + ")";
        }

        $("#fileName").text(fileName);
        return true;
    });

    //Range 값 실시간 업데이트
    $("#temperature").on("input", function(){
        $("#temperatureVal").text($(this).val());
    });
    $("#topP").on("input", function(){
        $("#topPVal").text($(this).val());
    });
    $("#presencePenalty").on("input", function(){
        $("#presencePenaltyVal").text($(this).val());
    });

    //선택된 파일 활성화/비활성화
    $(document).on("click", ".fileName", function() {
        let active = $(this).hasClass("active");
        $(".fileName").removeClass("active");
        if(!active) {
            $(this).addClass("active");
        }

        let activeElement = $(".fileName.active");
        if(activeElement.text()) {
            $("#UploadFieldset").prop("disabled", true);
            $("#fileSelectedName").html(activeElement.text() + `<span class="badge bg-secondary rounded-pill ms-auto cancelSelectBtn">선택 취소</span>`);
        } else {
            resetSelectedFile();
        }
    });

    $(document).on("click", ".cancelSelectBtn", function() {
        resetSelectedFile();
    });

    //선택된 질문 활성화/비활성화
    $(".question").on("click", function() {
        let active = $(this).hasClass("active");

        $(".question").removeClass("active");

        if(!active) $(this).addClass("active");

        if($(".question.active")?.hasClass("custom")) $("#customQuestion").prop("disabled", false);
        else $("#customQuestion").prop("disabled", true);
    });

    //파일/질문 해석 로직
    $("#btnSubmit").on("click", function(){
        //해석 중
        if(loading) {
            alert("해석 중입니다. 잠시만 기다려주세요.");
            return;
        }

        //첨부 파일 확인
        let attachment = $("#analyzeFile")[0].files[0];
        let fileName = $(".fileName.active").text();
        if(!attachment && !fileName) {
            alert("해석할 파일을 선택해주세요.");
            return;
        }

        //선택한 질문 없음
        let question = $(".question.active").text();
        let customQuestion = $("#customQuestion").val();
        if(!question) {
            alert("질문을 선택해주세요.");
            return;
        } else if(question === "질문 직접 입력" && !customQuestion) {
            alert("질문을 입력해주세요.");
            return;
        }

        loading = true;
        $("#LoadingText").show();

        let uploadYn = $("#uploadYn").is(":checked");
        let temperature = $("#temperature").val();
        let topP = $("#topP").val();
        let presencePenalty = $("#presencePenalty").val();

        let formData = new FormData();

        if(fileName) formData.append("fileName", fileName);
        else formData.append("attachment", attachment);

        formData.append("uploadYn", uploadYn);
        formData.append("question", question);
        formData.append("customQuestion", customQuestion);
        formData.append("temperature", temperature);
        formData.append("topP", topP);
        formData.append("presencePenalty", presencePenalty);
        formData.append("csrfmiddlewaretoken", window.CSRF_TOKEN);

        $.ajax({
            url: "/summarize",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                const converter = new showdown.Converter();
                $("#ResultContainer").html(converter.makeHtml(data.result));

                window.fileList = data.file_list;
                updateFileList(fileList);

                loading = false;
                $("#LoadingText").hide();
            },
            error: function(xhr, ajaxOptions, error) {
                console.log(xhr);
                alert('오류가 발생했습니다. 다시 시도하세요.');
                loading = false;
                $("#LoadingText").hide();
            }
        })
    });
});

//표시할 파일 크기 계산 로직
const getFileSize = function(file) {
    let size = file.size;
    let scale = ["B", "KB", "MB", "GB", "TB"];
    let scaleIndex = 0;

    while(size > 1024 && scaleIndex < scale.length) {
        size = Math.round(size / 1024 * 100) / 100
        scaleIndex++;
    }

    return size + scale[scaleIndex];
}

//모달에 있는 파일 목록 업데이트
const updateFileList = function(fileList) {
    const fileListHtml = (fileName, activeName) => {return `<li class="list-group-item list-group-item-secondary fileName ` + ((fileName === activeName) ? `active` : ``) + `">` + fileName + `</li>`}
    const emptyHtml = `<li class="list-group-item list-group-item-light">(클라우드에 저장된 파일이 없습니다)</li>`;
    const fileListContainer = $("#fileListContainer");
    const activeName = $(".fileName.active").text();

    fileListContainer.html("");
    if(fileList.length) {
        fileList.forEach(fileName => {
            fileListContainer.append(fileListHtml(fileName, activeName));
        });
    } else {
        fileListContainer.append(emptyHtml);
    }
}

//선택된 클라우드 파일 선택 취소
const resetSelectedFile = function() {
    $(".fileName").removeClass("active");
    $("#UploadFieldset").prop("disabled", false);
    $("#fileSelectedName").text("(선택된 파일이 없습니다.)");
}
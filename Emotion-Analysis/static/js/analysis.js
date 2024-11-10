$(document).ready(function() {
    $('#singleAnalysisForm').on('submit', function(event) {
        event.preventDefault();
        singleAnalysisSubmit();
    });

    $('#batchAnalysisForm').on('submit', function(event) {
        event.preventDefault();
        batchAnalysisSubmit();
    });

    // 监听单项分析的文本区域内容变化，动态调整高度
    $('#single_text').on('input', function() {
        autoResizeTextarea(this);
    });
});

function singleAnalysisSubmit() {
    var formData = $('#singleAnalysisForm').serialize();

    $.ajax({
        type: 'POST',
        url: singleAnalysisUrl,  // 将 URL 参数作为变量
        data: formData,
        success: function(response) {
            $('#single_result').html('<h3>情感倾向为: ' + (response.result ? response.result : '未分析') + '</h3>');
            $('html, body').animate({ scrollTop: $('#single_result').offset().top }, 500);
        },
        error: function(error) {
            $('#single_result').html('<h3>分析失败，请重试。</h3>');
        }
    });
}

function batchAnalysisSubmit() {
    var formData = $('#batchAnalysisForm').serialize();

    $.ajax({
        type: 'POST',
        url: batchAnalysisUrl,  // 将 URL 参数作为变量
        data: formData,
        success: function(response) {
            let resultHTML = '<h3>批量分析结果:</h3><ul>';
            response.results.forEach(function(line) {
                resultHTML += '<li>' + line + '</li>';
            });
            resultHTML += '</ul>';
            $('#batch_result').html(resultHTML);
            $('html, body').animate({ scrollTop: $('#batch_result').offset().top }, 500);
        },
        error: function(error) {
            $('#batch_result').html('<h3>批量分析失败，请重试。</h3>');
        }
    });
}

// 自动调整文本框高度的函数
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto'; // 重置高度，防止高度累计
    textarea.style.height = textarea.scrollHeight + 'px'; // 设置高度为内容的高度
}

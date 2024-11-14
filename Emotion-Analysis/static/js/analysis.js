$(document).ready(function() {
    const submitButton = document.getElementById('text_submit');
    const textarea = document.getElementById('single_text');

    // 检查文本框是否为空
    function checkFormValidity() {
        submitButton.disabled = textarea.value.trim() === ''; // 如果文本框为空，禁用按钮
    }

    // 页面加载时立即检查一次按钮状态
    checkFormValidity();

    // 监听文本框输入事件
    textarea.addEventListener('input', function() {
        checkFormValidity();
        autoResizeTextarea(this); // 调用自动调整文本框高度
    });

    // 监听表单提交
    $('#singleAnalysisForm').on('submit', function(event) {
        event.preventDefault();
        singleAnalysisSubmit();
    });
});

// 单项分析的提交函数
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

// 自动调整文本框高度的函数
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto'; // 重置高度，防止高度累计
    textarea.style.height = textarea.scrollHeight + 'px'; // 设置高度为内容的高度
}

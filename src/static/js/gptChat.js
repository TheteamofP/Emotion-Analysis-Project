$(document).ready(function () {
    const maxTextareaHeight = 200;
    const defaultTextareaHeight = 100;
    const $textInput = $('#text');
    const $chatContainer = $('#chat-container');
    const $typingIndicator = $('#typing-indicator');

    // 清空聊天记录
    localStorage.removeItem('chatHistory');

    // 自动调整文本框高度
    function autoResizeTextarea() {
        $textInput.css('height', 'auto');
        let newHeight = Math.max(defaultTextareaHeight, $textInput[0].scrollHeight);
        $textInput.css({
            height: newHeight > maxTextareaHeight ? `${maxTextareaHeight}px` : `${newHeight}px`,
            overflowY: newHeight > maxTextareaHeight ? 'auto' : 'hidden'
        });
    }

    // 添加聊天消息
    function addMessage(content, type) {
        const time = new Date().toLocaleTimeString();
        const formattedContent = content.replace(/\n/g, '<br>');
        const messageClass = type === 'user' ? 'user-message' : 'ai-message';
        const message = `
            <div class="message ${messageClass}">
                <div class="message-content">${formattedContent}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        $chatContainer.append(message);
        saveChatHistory(content, type);
        scrollToBottom();
    }

    // 滚动到底部
    function scrollToBottom() {
        $chatContainer.animate({ scrollTop: $chatContainer[0].scrollHeight }, 300);
    }

    // 保存聊天记录
    function saveChatHistory(content, type) {
        const history = getChatHistory();
        history.push({ content, type, timestamp: new Date().toISOString() });
        localStorage.setItem('chatHistory', JSON.stringify(history));
    }

    // 获取聊天记录
    function getChatHistory() {
        return JSON.parse(localStorage.getItem('chatHistory') || '[]');
    }

    // 提交表单
    $('#gpt-form').on('submit', function (event) {
        event.preventDefault();
        const userInput = $textInput.val().trim();
        if (!userInput) return;

        addMessage(userInput, 'user');
        $textInput.val('').css('height', `${defaultTextareaHeight}px`);
        $typingIndicator.show();

        const chatHistory = getChatHistory();

        $.ajax({
            type: 'POST',
            url: gptSuggestionUrl,
            data: {
                text: userInput,
                history: JSON.stringify(chatHistory)
            },
            success: function (response) {
                $typingIndicator.hide();
                addMessage(response.result.error || response.result.gpt_response, response.result.error ? 'error' : 'ai');
                scrollToBottom();
            },
            error: function () {
                $typingIndicator.hide();
                addMessage('调用 GPT API 出错，请重试', 'error');
            }
        });
    });

    // 处理 Enter 和 Shift + Enter
    $textInput.on('keydown', function (event) {
        if (event.key === 'Enter') {
            if (event.shiftKey) {
                event.preventDefault();
                const cursorPos = this.selectionStart;
                const text = $textInput.val();
                $textInput.val(text.substring(0, cursorPos) + "\n" + text.substring(cursorPos));
                this.selectionStart = this.selectionEnd = cursorPos + 1;
            } else {
                event.preventDefault();
                $('#gpt-form').submit();
            }
        }
    }).on('input', autoResizeTextarea);

    // 监听任意键盘输入聚焦输入框
    $(document).on('keydown', function () {
        if (!$textInput.is(':focus')) {
            $textInput.focus();
        }
    });

    // 获取 URL 中的 "text" 参数
    const presetText = new URLSearchParams(window.location.search).get('text');
    if (presetText) {
        $textInput.val(decodeURIComponent(presetText));
        autoResizeTextarea();
        $('html, body').animate({
            scrollTop: $textInput.offset().top
        }, 300);
    }

    // 监听 URL hash 并调整文本框高度
    if (window.location.hash === '#gpt_suggestion') {
        setTimeout(autoResizeTextarea, 100);
    }

    // 窗口大小改变时调整文本框高度
    $(window).on('resize', autoResizeTextarea);

    // 清空对话按钮
    $('#clear-chat').click(function () {
        if (confirm('确定要清空所有对话记录吗？')) {
            localStorage.removeItem('chatHistory');
            $chatContainer.empty();
        }
    });
});

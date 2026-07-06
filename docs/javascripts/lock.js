document.addEventListener("DOMContentLoaded", function () {
    // التحقق من وجود وسم التشفير في الصفحة الحالية
    if (document.body.innerHTML.includes("<!-- encrypt -->") || document.querySelector('meta[name="encrypt"]')) {
        
        // التحقق مما إذا كان المستخدم قد أدخل كلمة المرور مسبقاً في هذه الجلسة
        if (sessionStorage.getItem("site_authorized") !== "true") {
            
            // إخفاء المحتوى الأصلي فوراً لحمايته
            const originalContent = document.querySelector(".md-content");
            if (originalContent) {
                originalContent.style.display = "none";
                
                // إنشاء واجهة طلب كلمة المرور الأنيقة المتوافقة مع الـ Dark/Light Mode
                const promptContainer = document.createElement("div");
                promptContainer.style.cssText = "text-align: center; padding: 50px 20px; max-width: 400px; margin: 100px auto; border: 1px solid var(--md-typeset-table-color); border-radius: 8px; background: var(--md-code-bg-color);";
                
                promptContainer.innerHTML = `
                    <h2 style="margin-bottom: 20px; color: var(--md-typeset-color);">🔒 محتوى محمي</h2>
                    <p style="margin-bottom: 20px; font-size: 14px;">هذا الدرس خاص، يرجى إدخال كلمة المرور للمتابعة.</p>
                    <input type="password" id="site-pass" placeholder="أدخل كلمة المرور هنا..." style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 15px; text-align: center; direction: ltr;">
                    <button id="submit-pass" style="background: var(--md-accent-color); color: #fff; border: none; padding: 10px 25px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">دخول</button>
                `;
                
                originalContent.parentNode.insertBefore(promptContainer, originalContent);
                
                // دالة التحقق من كلمة المرور
                const checkPassword = () => {
                    const enteredPass = document.getElementById("site-pass").value;
                    if (enteredPass === "123456") { // <-- ضع كلمة المرور التي تريدها هنا
                        sessionStorage.setItem("site_authorized", "true");
                        promptContainer.remove();
                        originalContent.style.display = "block";
                    } else {
                        alert("كلمة مرور خاطئة! يرجى المحاولة مجدداً.");
                    }
                };
                
                document.getElementById("submit-pass").addEventListener("click", checkPassword);
                document.getElementById("site-pass").addEventListener("keypress", function (e) {
                    if (e.key === "Enter") checkPassword();
                });
            }
        }
    }
});
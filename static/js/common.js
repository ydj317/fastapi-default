/**
 * common.js
 */

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function deleteAllCookies() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name.trim() + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }
}

async function callApi(method, apiUrl, formData) {
    try {
        const response = await fetch(apiUrl, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: formData ? JSON.stringify(formData) : null
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        throw new Error(error.message || 'API 호출 실패');
    }
}
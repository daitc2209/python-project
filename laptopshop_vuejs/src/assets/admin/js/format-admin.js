export function formatDate(date) {
    const formattedDate = new Date(date);
    const hours = ('0' + formattedDate.getHours()).slice(-2);
    const minutes = ('0' + formattedDate.getMinutes()).slice(-2);
    const day = ('0' + formattedDate.getDate()).slice(-2);
    const month = ('0' + (formattedDate.getMonth() + 1)).slice(-2);
    const year = formattedDate.getFullYear();
    return `${day}-${month}-${year} ${hours}:${minutes}`;
};

export function formatCurrency(value) {
    const formatter = new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    });
    return formatter.format(value);
};
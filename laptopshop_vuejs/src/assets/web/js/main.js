
let dec = document.querySelector(".quantity .pro-qty .dec");
let inc = document.querySelector(".quantity .pro-qty .inc");

export function decFunction(id){
	let textInput = document.querySelector(".quantity .pro-qty .id-"+id);
	let quanty = parseInt(textInput.value);
	return textInput.value = quanty<=1 ? 1 : quanty-1;
}
export function incFunction(id){
	let textInput = document.querySelector(".quantity .pro-qty .id-"+id);
	let quanty = parseInt(textInput.value);
	return textInput.value = quanty+1;
};

export function formatDate(date) {
    const formattedDate = new Date(date);
    const hours = ('0' + formattedDate.getHours()).slice(-2);
    const minutes = ('0' + formattedDate.getMinutes()).slice(-2);
    const day = ('0' + formattedDate.getDate()).slice(-2);
    const month = ('0' + (formattedDate.getMonth() + 1)).slice(-2);
    const year = formattedDate.getFullYear();
    return `${hours}:${minutes} ${day}/${month}/${year}`;
};
export function formatCurrency(value) {
    const formatter = new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    });
    return formatter.format(value);
};
export function getGenderDisplay(gender) {
    const stateMap = {
        MALE: "NAM",
        FEMALE: "NỮ"
    };
    return stateMap[gender] || "";
};
export function getStateCheckoutDisplay(stateCheckout) {
    const stateMap = {
        0: "Chưa thanh toán",
        1: "Đã thanh toán"
    };
    return stateMap[stateCheckout] || "";
};
export function getStateOrderDisplay(stateOrder) {
    const stateMap = {
        0: "Đang xử lý",
        1: "Đang giao hàng",
        2: "Đã xác nhận",
        3: "Đã nhận",
        4: "Đã huỷ"
    };
    return stateMap[stateOrder] || "";
};

export function toast({ title = '',
            message = '',
            type = 'info',
            duration = 3000
        }) {
            const main = document.getElementById('toast')
            const delay = (duration / 1000).toFixed(2)  //lấy ra 2 số thập phân 
            const icons = {
                success: 'fas fa-check-circle',
                info: 'fas fa-info-circle',
                warning: 'fas fa-exclamation-circle',
                error: 'fa-solid fa-circle-xmark',
            }
            const toast = document.createElement('div')
            toast.classList.add('toast', `toast--${type}`)

            // auto remove toast
            const autoRemoveId = setTimeout(() => {
                    main.removeChild(toast)
                }, duration + 1000);

            //remove toast when click
            toast.onclick = function(e){
                if(e.target.closest('.toast__close'))   //closest: tìm class của chính nó, ko thấy thì nó sẽ tìm ra cha nó
                {
                    main.removeChild(toast)
                    clearTimeout(autoRemoveId)
                }
            }


            const icon = icons[type]    //truyền type của object vào 
            toast.style.animation = ` slideInLeft ease .3s, fadeOut linear 1s ${delay}s forwards`

            if (main) {
                toast.innerHTML = `
                    <div class="toast__icon">
                        <i class="${icon}"></i>
                    </div>
    
                    <div class="toast__body">
                        <h3 class="toast__title">${title}</h3>
                        <p class="toast__msg">${message}</p>
                    </div>
                    <div class="toast__close">
                         <i class="fas fa-times"></i>
                    </div>
                `;
                main.appendChild(toast); //truyền toast vào main

            }
        }

export function showSuccessToast(message) {
    toast({
        title: 'Success',
        message: message,
        type: 'success',
        duration: 1000
    })
}

export function showWarnToast(mess) {
    toast({
        title: 'Warning',
        message: mess,
        type: 'warning',
        duration: 1000
    })
}
export function showErrorToast() {
    toast({
        title: 'Error',
        message: 'Có lỗi rồi bro !!!',
        type: 'error',
        duration: 1000
    })
}

export function showErrorToastMess(message) {
    toast({
        title: 'Error',
        message: message,
        type: 'error',
        duration: 1000
    })
}

export function showInforToast() {
    toast({
        title: 'Info',
        message: 'Cập nhật thành công !!!',
        type: 'info',
        duration: 1000
    })
}

export function owlCarousel(data){
    $(data).owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        items: 4,
        dots: false,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        smartSpeed: 1000,
        autoHeight: false,
        autoplay: true,
        responsive: {
        0: {
            items: 1,
        },
        360: {
            items: 2,
        },
        576: {
            items: 2,
        },
        992: {
            items: 4,
        },
        1200: {
            items: 4,
        }
        }
    });
}
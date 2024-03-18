import axios from "axios";

const checkOutApi = {
    getBill: async (id) =>{
        const res = await axios.get(`/orders/getBill?id=`+id);
        return res.data
    },
    getBillVNPAY: async (vnp_Amount,vnp_BankCode,vnp_CardType,
        vnp_OrderInfo,vnp_PayDate,vnp_ResponseCode,vnp_TxnRef)=>{
        const res = await axios.get(`/checkout/vnpay/info?vnp_Amount=`+vnp_Amount
                +`&vnp_BankCode=`+vnp_BankCode
                +`&vnp_CardType=`+vnp_CardType
                +`&vnp_OrderInfo=`+vnp_OrderInfo
                +`&vnp_PayDate=`+vnp_PayDate
                +`&vnp_ResponseCode=`+vnp_ResponseCode
                +`&vnp_TxnRef=`+vnp_TxnRef);
        return res.data
    },

    sendEmail: async (orderCode)=>{
        const res = await axios.post("/checkout/orderConfirm?codeOrder="+orderCode)
        return res.data
    }
}

export default checkOutApi
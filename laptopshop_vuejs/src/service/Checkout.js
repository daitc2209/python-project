import axios from "axios";

const checkOutApi = {
    getBill: async (id) =>{
        const res = await axios.get(`/orders/getBill?id=`+id);
        return res.data
    },

    sendEmail: async (orderCode)=>{
        const res = await axios.post("/checkout/orderConfirm?codeOrder="+orderCode)
        return res.data
    }
}

export default checkOutApi
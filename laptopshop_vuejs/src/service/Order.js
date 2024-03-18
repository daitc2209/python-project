import axios from "axios";

const orderApi = {
    getOrder: async ()=>{
        const res = await axios.get(`orders`);
        return res.data
    },
    postOrder: async (data)=>{
        const res = await axios.post(`orders`,data);
        return res
    },
    getBill: async (id)=>{
        const res = await axios.get(`checkout/getBill?id=`+id);
        return res.data;
    },

    // Admin
    getAllOrderByStatus: async ()=>{
        const res = await axios.get(`admin/order/total-order-status`)
        return res.data
    },
    getListOrderByStatus: async (page,search_text,status)=>{
        const res = await axios.get("admin/order", {params:{page:page, search_text:search_text, status:status}})
        return res.data
    },
    findByRangeDay: async (page,data)=>{
        const res = await axios.post("admin/order/range-day?page="+page,data)
        return res.data
    },
    getOrderById: async (id)=>{
        const res = await axios.get("admin/order/"+id)
        return res.data
    },
    verify: async (id,status)=>{
        const res = await axios.post("admin/order/verify?id="+id+"&status="+status)
        return res.data;
    },

}

export default orderApi
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
        const res = await axios.get(`admin/orders/get-all-status`)
        return res.data
    },
    getListOrderByStatus: async (search_text,status)=>{
        const res = await axios.get("admin/orders/get-all-orders", {params:{search_text:search_text, status:status}})
        return res.data
    },
    getOrderById: async (id)=>{
        const res = await axios.get("admin/orders/"+id)
        return res.data
    },
    verify: async (id,status)=>{
        const res = await axios.post("admin/orders/update-status/"+id+"/"+status)
        return res.data;
    },

}

export default orderApi
import axios from "axios"

const cartApi = {
    addToCart: async (cart)=>{
        const res = await axios.post(`carts/add-to-cart?product_id=`+cart.productId+`&num=`+cart.num);
        return res.data
    },

    GetItemInCart: async ()=>{
        const res = await axios.get(`carts`);
        return res.data
    },

    editItemCart: async (id,num)=>{
        const res = await axios.get(`carts/edit-cart/${id}?num=${num}`)
        return res.data
    },

    deleteItemCart: async (id)=>{
        const res = await axios.get(`carts/delete-cart/${id}`)
        return res.data
    },

    clearCart: async ()=>{
        const res = await axios.get(`carts/clear-cart`)
        return res.data
    },
}

export default cartApi
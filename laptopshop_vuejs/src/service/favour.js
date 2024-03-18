import axios from "axios"

const favourApi = {
    addToFavour: async (id)=>{
        const res = await axios.post(`favors/add-to-favor?product_id=`+id);
        return res.data
    },

    GetItemInFavour: async ()=>{
        const res = await axios.get(`favors`);
        return res.data
    },

    deleteItemFavour: async (id)=>{
        const res = await axios.get(`favors/delete-favor?id=`+id)
        return res.data
    }
}

export default favourApi
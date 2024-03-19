import axios from "axios";

const revenueApi = { 
    getCard: async () => {
        const res = await axios.get(`/admin/card`)
        return res.data
    }
}

export default revenueApi;
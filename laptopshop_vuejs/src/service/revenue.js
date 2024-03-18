import axios from "axios";

const revenueApi = { 
    getRevenueCategories: async () => {
        const res = await axios.get(`/admin/revenue/categories`)
        return res.data
    },

    getRevenue: async () => {
        const res = await axios.get(`/admin/revenue`)
        return res.data
    },

    getRevenueYear: async (year) => {
        const res = await axios.get(`/admin/revenue/`+year)
        return res.data
    },

    getRevenueProducts: async () => {
        const res = await axios.get(`/admin/revenue/products`)
        return res.data
    },

    getStatistical: async (data) =>{
        const res = await axios.post(`/admin/revenue/range-day`,data)
        return res.data
    },

    getCard: async () => {
        const res = await axios.get(`/admin/revenue/card`)
        return res.data
    }
}

export default revenueApi;
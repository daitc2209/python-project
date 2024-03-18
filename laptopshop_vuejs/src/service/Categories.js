import axios from "axios"

const categoriesApi = {
    getAllCategories: async () => {
        const res = await axios.get("admin/category/findAll")
        return res.data
    },

    getListCategories: async (page,search) => {
        const res = await axios.get("admin/category",{params: { page:page, search:search }})
        return res.data
    },

    getEditCategories: async (id) => {
        const res = await axios.get("admin/category/edit/"+id)
        return res.data
    },

    postEditCategories: async (data) => {
        const res = await axios.post("admin/category/edit",data)
        return res.data
    },

    postAddCategories: async (data) => {
        const res = await axios.post("admin/category/add",data)
        return res.data
    },

    deleteCategories: async (id) => {
        const res = await axios.post("admin/category/delete?id="+id)
        return res.data
    },

}

export default categoriesApi
import axios from "axios"
 
const brandsApi = {
    
    // lấy thương hiệu để hiển thị ở trang chủ
    getBrands: async () =>{
        const res = await axios.get("findAllBrand")
        return res.data
    },

    getAllBrands: async () => {
        const res = await axios.get("admin/brand/findAll")
        return res.data
    },

    getListBrands: async (page,search) => {
        const res = await axios.get("admin/brand",{params: {search:search , page:page}})
        return res.data
    },

    getEditBrands: async (id) => {
        const res = await axios.get("admin/brand/edit/"+id)
        return res.data
    },

    postEditBrands: async (data) => {
        const res = await axios.post("admin/brand/edit",data)
        return res.data
    },

    postAddBrands: async (data) => {
        const res = await axios.post("admin/brand/add",data)
        return res.data
    },

    deleteBrands: async (id) => {
        const res = await axios.post("admin/brand/delete?id="+id)
        return res.data
    },


}

export default brandsApi
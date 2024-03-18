import axios from "axios"

const productApi = {
    getFilterProduct: async (sort, category, brand, minPrice, maxPrice ,page) => {
        const res = await axios.get(`store`,{ params: { 
            sort: sort, category: category,
            brand: brand, minPrice:minPrice, maxPrice:maxPrice, page: page }});
        
            return res.data
    },

    getAllProduct: async () => {
        const res = await axios.get("products");
        return res.data
    },

    getSameProduct: async () =>{
        const res = await axios.get("products?page=1&limit=10")
        return res.data
    },

    getProductById: async (id) => {
        const res = await axios.get(`products/`+id);
        return res.data
    },

    getListProduct: async (page,search) =>{
        const res = await axios.get(`admin/product`, 
            {params: {page:page,search_text:search.search_text, categoryId:search.categoryId,brandId:search.brandId}})
        return res.data
    },

    deleteProduct: async (id) => {
        const res = await axios.post(`admin/product/delete?id=`+id)
        return res.data
    },

    addProduct: async (data) => {
        const res = await axios.post(`admin/product/add`,data)
        return res.data
    },

    getEditProduct: async (id) => {
        const res = await axios.get(`admin/product/edit/${id}`)
        return res.data
    },

    postEditProduct: async (data) => {
        const res = await axios.post(`admin/product/edit`,data)
        return res.data
    },

    stateProduct: async (id,state) => {
        const res = await axios.post(`admin/product/lock_unlock?id=${id}&state=${state}`)
        return res.data
    }
}

// export default new Products();
export default productApi;
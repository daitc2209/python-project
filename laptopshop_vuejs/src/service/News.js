import axios from "axios";

const newsApi = {
    getNews: async (page)=>{
        if(page == "" || page == null)
            page = 1
        const res = await axios.get(`news?page=`+page);
        return res.data
    },

    getDetailNews: async (id,page) => {
        if(page == "" || page == null)
            page = 1
        const res = await axios.get(`news/detail?id=${id}&page=`+page);
        return res.data;
    },

    getNewsAdmin: async (page,search) => {
        const res = await axios.get(`admin/news`,{params: {search:search , page:page}})
        return res.data
    },

    getEditNewsAdmin: async (id)=>{
        const res = await axios.get(`admin/news/edit/${id}`)
        return res.data
    },

    postEditNewsAdmin: async (data) =>{
        const res = await axios.post(`admin/news/edit`,data)
        return res.data
    },

    postAddNewsAdmin: async (data)=>{
        const res = await axios.post("admin/news/add",data)
        return res.data
    },

    deleteNewsAdmin: async (id)=>{
        const res = await axios.post("admin/news/delete?id="+id)
        return res.data
    }
}

export default newsApi
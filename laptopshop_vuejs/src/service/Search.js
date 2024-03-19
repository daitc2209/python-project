import axios from "axios";

const searchApi = {
    Search: async (search_text)=>{
        const res = await axios.get("products/",{params: {search_text:search_text}}) 
        return res.data
    }
}
export default searchApi 
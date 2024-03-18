import axios from "axios";

const searchApi = {
    Search: async (input)=>{
        const res = await axios.get("search",input)
        return res.data
    }
}
export default searchApi
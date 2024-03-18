
import axios from "axios"

const userApi = {

    signUp: async (data)=>{
        try {
            const response = await axios({
                method: "post",
                url: `http://127.0.0.1:8000/api/v1/users/signup`,
                data: data,
            });
        if (response.status == 200) {
            return true
        }
        } catch (err) {
            console.log(err.response);
        }
    },

    login: async(data)=>{
        const config = {
            headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            },
        };
        const params = new URLSearchParams();
        params.append("username", data.username);
        params.append("password", data.password);
        const response = await axios({
            method: "post",
            url: `http://127.0.0.1:8000/api/v1/users/token`,
            data: params,
            config,
        });
        return response
    },

    getInfo: async ()=>{
        const res = await axios.post('me') 
        return res.data
    },

    getPurchaseHistory: async (status)=>{
        const res = await axios.get('orders/purchase-history?status='+status);
        return res.data
    },

    postPurchaseHistory: async (id,status)=>{
        const res = await axios.post(`orders/purchase-history?id=`+id+`&status=`+status)
        return res.data
    },

    postSendMailCancelled: async (codeOrder)=>{
        const res = await axios.post(`purchase-history/send-mail-cancelled?codeOrder=${codeOrder}`)
        return res.data
    },

    findByRangeDay: async (data)=>{
        const res = await axios.post(`purchase-history/range-day`,data)
        return res.data
    },

    getTotalOrderReceived: async ()=>{
        const res = await axios.get('orders/purchase-history/totalOrder');
        return res.data
    },

    postProfile: async (data)=>{
        const res = await axios.patch('users/updateme', data)
        return res.data
    },

    getProfile: async ()=>{
        const res = await axios.get('users/me')
        return res
    },

    postChangePW: async (oldPW, newPW)=>{
        const res = await axios.post('users/profile/change-password?oldPW='+oldPW+'&newPW='+newPW)
        return res.data
    },

    // Admin
    getListUserAdmin: async (page, fullname,sex,address,email,stateUser,authType)=>{
        const res = await axios.get('admin/user',
            {params: {fullname:fullname,sex:sex,address:address,
                    email:email,stateUser:stateUser,authType:authType,page:page}}) 
        return res.data
    },

    getListAdmin: async (page, fullname,sex,address,email,stateUser,authType)=>{
        const res = await axios.get('admin/user/getAdmin',
            {params: {fullname:fullname,sex:sex,address:address,
                    email:email,stateUser:stateUser,authType:authType,page:page}}) 
        return res.data
    },

    addUser: async (data)=>{
        const res = await axios.post("admin/user/add",data)
        return res.data
    },

    getEditUser: async (id)=>{
        const res = await axios.get("admin/user/edit/"+id)
        return res.data
    },

    postEditUser: async (data)=>{
        const res = await axios.post("admin/user/edit",data)
        return res.data
    },

    lockUser: async (id)=>{
        const res = await axios.post("admin/user/lock?id="+id)
        return res.data
    },

    unlockUser: async (id)=>{
        const res = await axios.post("admin/user/unlock?id="+id)
        return res.data
    },

    deleteUser: async (id)=>{
        const res = await axios.post("admin/user/delete?id="+id)
        return res.data
    },
}

export default userApi;
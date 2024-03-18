import axios from "axios"

const ForgotPWApi = {
    handleRequestForgorPW: async (email)=>{
        const res = await axios.post(`/auth/forgot-password?email=`+email);
        return res.data
    },

    checkTokenPW: async (token)=>{
        const res = await axios.get(`/auth/reset-password?token=`+token);
        return res.data
    },

    resetPW: async (token,newPW)=>{
        const res = await axios.post(`/auth/reset-password?token=${token}&newPW=${newPW}`)
        return res.data
    }
}

export default ForgotPWApi
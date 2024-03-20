import axios from "axios"
axios.defaults.headers.get['Accepts'] = 'application/json';
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.common['Access-Control-Allow-Method'] = '*';
axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept';
axios.defaults.baseURL = 'http://localhost:8000/api/v1/'
if(sessionStorage.getItem("jwtToken") != null && sessionStorage.getItem("jwtToken") != ""){
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + sessionStorage.getItem("jwtToken");
}

<template>
  <div>
    <head>
      <title>Cửa hàng</title>
    </head>
    <div id="toast">
    </div>
    <section class="store">
      <div class="container">
        <div class="row">
          <div>
            <div class="breadcrumbs d-flex flex-row align-items-center col-12">
              <ul>
                <li><a href="/home">Trang chủ</a></li>
                <li class="active"><a href="#"><i class="fa fa-angle-right" aria-hidden="true"></i>Cửa hàng</a></li>
              </ul>
            </div>
            <div id="formStore">
              <div class="product-list ">
                <div class="row col-12">
                  <template v-if="listProduct.length > 0">
                    <div class="product-item col-lg-3 col-md-6 col-sm-6 col-12 " v-for="item in listProduct"  :key="item.id">
                        <div class="product-item" >
                            <div class="pi-pic " >
                              <img :src="item.img" alt="">
                              <ul>
                                <li class="w-icon active">
                                  <a @click="addToCart(item._id)"><i class="fa-solid fa-cart-shopping"></i></a>
                                </li>
                                <li class="w-icon active">
                                  <a @click="addToFavour(item._id)"><i class="fa-solid fa-heart"></i></a>
                                </li>
                                <li class="quick-view"><a :href="'/store/' + item._id">+ Quick View</a></li>
                              </ul>
                            </div>
                            <div class="pi-text">
                              <h5>{{ item.name }}</h5>
                              <div class="product-price">
                                {{ formatCurrency(item.price - (item.price * item.discount / 100)) }}
                                <del v-if="item.discount > 0">{{ formatCurrency(item.price) }}</del>
                            </div>
                            </div>
                            <div class="home-product-item__favourite">
                                <span>Giảm {{ item.discount }}%</span>
                            </div>
                        </div>
                    </div>
                  </template>
                  <div v-else>
                    <div class="col-lg-3 col-sm-6 col-6">
                      Không có sản phẩm phù hợp
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
  
<script>
import { showSuccessToast, showErrorToast, showWarnToast, showErrorToastMess, formatCurrency } from "../../../assets/web/js/main";
import productApi from '../../../service/Product';
import cartApi from '../../../service/Cart';
import favourApi from '../../../service/favour';
export default {
  data() {
    return {
      formFilterProduct: {
        sort: 'low-high',
        cateogryName: 'all',
        brandName: 'all',
        minPrice: 0,
        maxPrice: 30000000
      },
      currentPage: '',
      paginationButtons:[],
      listProduct: [],
      category: [],
      brand: [],
      totalPages: '',
      errorMsg: '',
      success: '',
      cart:{
        productId:'',
        num:'',
      }
    };
  },
  methods: {
    formatCurrency,
    async getFilterProduct(page){
      try{
        const res = await productApi.getAllProduct()
        this.listProduct = res.data;
      }
      catch(err){
        console.log("loi store Get: "+err)
      }
    },
    async addToCart(id){
      try{
        if(sessionStorage.getItem("login"))
        {
          this.cart.productId=id
          this.cart.num = 1
          await cartApi.addToCart(this.cart)
          showSuccessToast('Thêm vào giỏ hàng thành công')
        }
        else{
          sessionStorage.setItem("err",true)
          this.$router.push("/auth/sign-in")
        }
      }catch(err){
        showErrorToastMess('Thêm vào giỏ hàng thất bại')
        this.$router.push("/auth/sign-in")
      }
    },
    async addToFavour(id){
      if(sessionStorage.getItem("login"))
      {
        const res = await favourApi.addToFavour(id)
        if(res.responseCode == 1) 
          showSuccessToast('Đã thêm sản phẩm vào yêu thích !!')
        
        if(res.responseCode == 2)
          showWarnToast('Sản phẩm đã có trong yêu thích !!')
      }
      else{
        sessionStorage.setItem("err",true)
        this.$router.push("/auth/sign-in")
      }
    },
    async loadProducts(page) {
      try{
        const res = await productApi.getFilterProduct(
          this.formFilterProduct.sort,
          this.formFilterProduct.cateogryName,
          this.formFilterProduct.brandName,
          this.formFilterProduct.minPrice,this.formFilterProduct.maxPrice,page)

          this.listProduct = res.data.listProduct
          this.brand = res.data.brand
          this.category = res.data.category
          this.totalPages = res.data.totalPages
          this.currentPage = res.data.currentPage
      }
      catch(err) {console.log("loi store pagination !!!!")}
		},
    initPrice(){
      let timeout = null;
      const delay = 500;
      $("#price-range-slider").slider({
        range: true,
        min: 0,
        max: 30000000,
        values: [this.formFilterProduct.minPrice, this.formFilterProduct.maxPrice],
        slide: (event, ui) => {
          this.formFilterProduct.minPrice = ui.values[0];
          this.formFilterProduct.maxPrice = ui.values[1];
          clearTimeout(timeout); // Xóa timeout hiện tại (nếu có)
          timeout = setTimeout(() => {
            this.currentPage=1
            this.getFilterProduct(1);
          }, delay);
        }
      });
    },
  },
   mounted() {
     this.getFilterProduct(1);
     this.initPrice();
     if (sessionStorage.getItem("cart-empty")==1)
     {
        let mess = 'Giỏ hàng không có sản phẩm !!'
        showErrorToastMess(mess)
        sessionStorage.removeItem("cart-empty")
     }
  },
};
</script>
  
<style>

</style>
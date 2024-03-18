<template>
    <div>

        <head>
            <title>Yêu thích</title>
        </head>
        <div id="toast">
    </div>
        <div class="breadcrumbs d-flex flex-row align-items-center col-12 container  mt-2">
            <ul class="m-0">
                <li><a href="/home">Trang chủ</a></li>
                <li class="active"><a href="#"><i class="fa fa-angle-right" aria-hidden="true"></i>Yêu thích</a></li>
            </ul>
        </div>

        <section class="shopping-cart ">
            <div class="container">
                <div class="row">
                    <div class="col-lg-12">
                        <div class="cart-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th>Tên sản phẩm</th>
                                        <th>Giới thiệu</th>
                                        <th>Giảm giá</th>
                                        <th>Giá</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="listFavour != null && listFavour !=''">
                                        <tr v-for="item in listFavour" :key="item._id">
                                            <td class="cart-pic first-row"> <img :src="item.img" alt="Product Image" /></td>
                                            <td class="cart-title first-row">
                                                <router-link :to="`/store/`+item.product_id"><h5 style="color: blue; word-break: break-word;">{{ item.name }}</h5></router-link>
                                            </td>
                                            <td class="cart-title first-row">
                                                <h4 class="item-description">{{ item.description }}</h4>
                                            </td>
                                            <td class="discount first-row">
                                                <h5>{{ item.discount }}%</h5>
                                            </td>
                                            <td class="p-price first-row">
                                                <h5>{{ formatCurrency(item.price) }}</h5>
                                            </td>
                                            <td><a><button class="btn-favour primary-btn pd-cart" @click="addToCard(item.product_id)">Thêm vào giỏ hàng</button></a></td>
                                            <td class="close-td first-row"><a @click="deleteItem(item._id)"><i
                                                        class="ti-close fa-sharp fa-solid fa-circle-xmark"></i></a></td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr>
                                            <td colspan="12">
                                                <h5 class="text-start p-4">Không có sản phẩm nào !!!</h5>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>
  
<script>
import { showSuccessToast, showErrorToastMess, formatCurrency } from "../../../assets/web/js/main";
import favourApi from "../../../service/favour";
import cartApi from "../../../service/Cart";
export default {
    data() {
        return {
            param: {
                err: ""
            },
            listFavour: [],
            cart: {
                productId: "",
                num:1
            }
        };
    },
    methods: {
        async addToCard(id) {
            try{
                this.cart.productId=id
                await cartApi.addToCart(this.cart)
                showSuccessToast("Đã thêm sản phẩm vào giỏ hàng !!")
            }catch(err){
                showErrorToastMess("Sản phẩm đã hết hàng !!")
                console.log("err o trang favour khi them gio hang: "+err)
            }
        },
        formatCurrency,
        async deleteItem(id) {
            try{
                await favourApi.deleteItemFavour(id)
                this.getItemInFavour()
                showSuccessToast('Xóa thành công sản phẩm khỏi yêu thích !')
            }catch(err){console.log("xoa khong thanh cong")}
        },
        async getItemInFavour() {
            try{
                const res = await favourApi.GetItemInFavour()
                this.listFavour = res.data
            }catch(err){console.log("loi trang cart !!! err: " + err) }
        }
    },
    mounted() {
        this.getItemInFavour();
    },
}
</script>
  
<style>
.btn-favour{
    width: 300px;
    height: 46px;
    border: none;
    border-radius: 10px;
}
.btn-favour:hover{
    background: #1c1c50;
    color: white;
}
</style>
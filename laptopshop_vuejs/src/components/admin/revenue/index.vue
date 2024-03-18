<template>
    <div>

        <head>
            <title>Thống kê danh mục</title>
        </head>
        <section class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-sm-6">
                        <h1>Thống kê danh mục</h1>
                    </div>
                    <div class="col-sm-6">
                        <ol class="breadcrumb float-sm-right">
                            <li class="breadcrumb-item"><a href='/admin/home'>Thống kê</a></li>
                            <li class="breadcrumb-item active">Doanh mục</li>
                        </ol>
                    </div>
                </div>
            </div>
        </section>

        <section class="search">
            <div id="toast">
            </div>
        </section>

        <section class="content d-flex">
            <!-- Default box -->
            <div class="card col-7">
                <div class="card-header">
                    <h3 class="card-title">Danh mục bán chạy</h3>
                </div>
                <div class="card-body">
                    <table class="text-center order-table">
                        <thead>
                            <tr>
                                <th>No.</th>
                                <th>Tên danh mục</th>
                                <th>Tổng sản phẩm bán được</th>
                                <th>Tổng doanh thu</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-if="revenue">
                                <tr :id="'trow_' + item.id" v-for="(item, index) in revenue" :key="item.id">
                                    <td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
                                    <td class="td2">
                                        <h6>{{ item.name }}</h6>
                                    </td>
                                    <td class="td3">
                                        <h6>{{ item.total_sell }}</h6>
                                    </td>
                                    <td class="td4">
                                        <h6>{{ formatCurrency(item.total_money) }}</h6>
                                    </td>
                                </tr>
                            </template>
                            <template v-else>
                                <tr>
                                    <td colspan="4">Không có bản ghi nào!!!</td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                    <template v-if="revenue">
                        <div class="pagination" id="pagination" v-if="paginationButtons.length >= 2">
                            <button v-for="page in paginationButtons" :key="page" :class="{ active: currentPage === page }"
                                @click="PaginationButton(page).handleClick()">
                                {{ page }}
                            </button>
                        </div>
                    </template>
                </div>
            </div>
            <div class="col-1"></div>
            <div class="col-4" style="width: 400px; height: 400px;">
                <canvas id="myChart"></canvas>
            </div>
        </section>
        
    </div>
</template>

<script>
import revenueApi from '../../../service/revenue';
import { formatCurrency } from "../../../assets/admin/js/format-admin";
import Chart from 'chart.js/auto'
export default {
    data() {
        return {
            revenue: [],
            currentPage: '',
            totalPage: '',
            paginationButtons: [],
        }
    },
    methods: {
        async getRevenueCategories(chart) {
            try{
                const res = await revenueApi.getRevenueCategories()
                this.revenue = this.sortedProducts(res.data.revenue)
                    
                this.updateChart(res.data.revenue, chart)
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        sortedProducts(data) {
            return data.slice().sort((a, b) => b.total_sell - a.total_sell);
        },

        formatCurrency,
        
        PaginationButton(page) {
            return {
                page,
                isActive: this.currentPage === page,
                handleClick: async () => {
                    console.log("page: " + page)
                    await this.loadOrders(page);
                },
            };
        },
        setupPagination(totalPage) {
            this.paginationButtons = [];

            let page_count = totalPage;
            for (let i = 1; i < page_count + 1; i++) {
                this.paginationButtons.push(i);
            }
        },

        updateChart(data, chart){
            const revenueData = data.map(item => item.total_money);
            const revenueLabels = data.map(item => item.name);

                // Tạo một mảng màu sắc tương ứng với số lượng label
                const colors = this.generateColors(revenueLabels.length);

                // Gán dữ liệu từ khu revenue vào data
                chart.data.datasets[0].data = revenueData;
                chart.data.labels = revenueLabels;
                chart.data.datasets[0].backgroundColor = colors;

                // Cập nhật biểu đồ
                chart.update();
        },

        generateColors(count) {
            const colors = [];

            for (let i = 0; i < count; i++) {
                const color = `rgb(${this.getRandomValue(0, 255)}, ${this.getRandomValue(0, 255)}, ${this.getRandomValue(0, 255)})`;
                colors.push(color);
            }

            return colors;
        },
        getRandomValue(min, max) {
            return Math.floor(Math.random() * (max - min + 1) + min);
        },
        init(){
            const ctx = document.getElementById("myChart")

            const data = {
                labels: [
                    'Red',
                    'Blue',
                    'Yellow',
                ],
                datasets: [{
                    label: 'Tổng thu nhập',
                    data: [300, 50, 100],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    hoverOffset: 4
                }]
            };

            const myChart = new Chart(ctx ,{
                type: 'pie',
                data: data,
            });

            this.getRevenueCategories(myChart)
        }
    },
    mounted() {
        if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="ROLE_ADMIN")
		{
			// window.location.href = "/auth/sign-in"
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth",true)
		}
		else
            this.init()
        
    }
}
</script>
  
<style></style>
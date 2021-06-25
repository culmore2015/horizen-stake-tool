<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 基础表格
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table
                    :data="tableData"
                    border
                    class="table"
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column prop="stkaddr" width="440" label="Stake地址"></el-table-column>
                <el-table-column prop="balance" width="220" align="center" label="钱包余额"></el-table-column>
                <el-table-column prop="id" label="ID" width="110" align="center"></el-table-column>
                <el-table-column prop="status" label="状态" width="110" align="center">
                    <template slot-scope="scope">
                        <el-tag v-if="scope.row.status==='active'" type="success">{{scope.row.status}}</el-tag>
                        <el-tag v-else-if="scope.row.status==='confirming'" type="">{{scope.row.status}}</el-tag>
                        <el-tag v-else type="danger">{{scope.row.status}}</el-tag>
                    </template>

                </el-table-column>
                <el-table-column prop="txid" width="220" label="TXID">
                    <template slot-scope="scope">
                        <a :href="'https://explorer.horizen.global/tx/'+scope.row.txid" target="_blank">
                            {{scope.row.txid.substring(0,12) + '...' + scope.row.txid.substring(scope.row.txid.length-12)}}
                        </a>
                    </template>
                </el-table-column>
                <el-table-column prop="paytos" min-width="220" label="分成信息">
                    <template slot-scope="scope">
                        <p v-for="it in scope.row.paytos">{{it.payto + ' - ' + it.pct + '%'}}</p>
                    </template>
                </el-table-column>
                <el-table-column prop="createdAt" width="220" align="center" label="创建时间(UTC)"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <!--                        <el-button-->
                        <!--                                type="text"-->
                        <!--                                icon="el-icon-edit"-->
                        <!--                                @click="handleEdit(scope.$index, scope.row)"-->
                        <!--                        >编辑-->
                        <!--                        </el-button>-->
                        <!--                        <el-button-->
                        <!--                                type="text"-->
                        <!--                                icon="el-icon-delete"-->
                        <!--                                class="red"-->
                        <!--                                @click="handleDelete(scope.$index, scope.row)"-->
                        <!--                        >删除-->
                        <!--                        </el-button>-->
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 编辑弹出框 -->
        <!--        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">-->
        <!--            <el-form ref="form" :model="form" label-width="70px">-->
        <!--                <el-form-item label="用户名">-->
        <!--                    <el-input v-model="form.name"></el-input>-->
        <!--                </el-form-item>-->
        <!--                <el-form-item label="地址">-->
        <!--                    <el-input v-model="form.address"></el-input>-->
        <!--                </el-form-item>-->
        <!--            </el-form>-->
        <!--            <span slot="footer" class="dialog-footer">-->
        <!--                <el-button @click="editVisible = false">取 消</el-button>-->
        <!--                <el-button type="primary" @click="saveEdit">确 定</el-button>-->
        <!--            </span>-->
        <!--        </el-dialog>-->
    </div>
</template>

<script>
    import {fetchZenSuperNodesStakeList} from '../../api/index';
    import {Config} from '../../config/config';
    import layer from "layui-layer";

    export default {
        name: 'basetable',
        data() {
            return {
                query: {
                    apikey: Config.apikey,
                },
                tableData: [],
                rawData: {},
                multipleSelection: [],
                delList: [],
                editVisible: false,
                form: {},
                idx: -1,
                id: -1
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                var index = layer.load(2);
                fetchZenSuperNodesStakeList(this.query).then(res => {
                    this.rawData = res;
                    var tableData = [];
                    this.rawData.forEach(function (it) {
                        // var paytoInfo = '';
                        // it.paytos.forEach(function (payto) {
                        //     paytoInfo += payto.payto + ' - ' + payto.pct
                        // });

                        // console.log(paytoInfo)
                        tableData.push({
                            stkaddr: it.stkaddr,
                            balance:it.balance,
                            status: it.status,
                            id: it.id,
                            txid: it.txid,
                            paytos: it.paytos,
                            createdAt: it.createdAt.substring(0, it.createdAt.lastIndexOf('.')).replace('T', ' ')
                        });
                    });
                    this.tableData = tableData;
                }).catch(() => {
                    layer.alert('网络错误，请重试!');
                }).finally(() => {
                    layer.close(index)
                });;
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 删除操作
            handleDelete(index, row) {
                // 二次确认删除
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                })
                    .then(() => {
                        this.$message.success('删除成功');
                        this.tableData.splice(index, 1);
                    })
                    .catch(() => {
                    });
            },
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            delAllSelection() {
                const length = this.multipleSelection.length;
                let str = '';
                this.delList = this.delList.concat(this.multipleSelection);
                for (let i = 0; i < length; i++) {
                    str += this.multipleSelection[i].name + ' ';
                }
                this.$message.error(`删除了${str}`);
                this.multipleSelection = [];
            },
            // 编辑操作
            handleEdit(index, row) {
                this.idx = index;
                this.form = row;
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                this.editVisible = false;
                this.$message.success(`修改第 ${this.idx + 1} 行成功`);
                this.$set(this.tableData, this.idx, this.form);
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            }
        }
    };
</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .red {
        color: #ff0000;
    }

    .mr10 {
        margin-right: 10px;
    }

    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>

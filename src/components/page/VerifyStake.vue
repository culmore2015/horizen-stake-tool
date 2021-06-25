<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 验证转账
                </el-breadcrumb-item>
                <el-breadcrumb-item>验证转账</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item label="API KEY">
                        <el-input v-model="form.apikey" disabled="disabled"></el-input>
                    </el-form-item>

                    <el-form-item label="TXID">
                        <el-input v-model="form.txid"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">立即验证</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import {Config} from '../../config/config';
    import {fetchZenSuperNodesVerifyStake} from '../../api/index';
    import layer from "layui-layer";

    export default {
        name: 'baseform',
        data() {
            return {
                form: {
                    apikey: Config.apikey,
                    txid: '',
                }
            };
        },
        methods: {
            onSubmit() {
                if (this.form.txid === '') {
                    this.$message.error('txid不能为空！');
                    return
                }
                var index = layer.load(2)
                fetchZenSuperNodesVerifyStake(this.form.apikey, this.form.txid)
                    .then(res => {
                        console.log(res);
                        layer.alert(res.message);
                    }).catch(() => {
                    layer.alert('网络错误，请重试!');
                }).finally(() => {
                    layer.close(index)
                });
            }
        }
    };
</script>
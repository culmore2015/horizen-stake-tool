import request from '../utils/request';
import qs from 'qs';

export const fetchZenSuperNodesStakeList = query => {
    return request.get('http://staketool.nodeasy.com:9090/stake/list?apikey=' + query.apikey);
};


export const fetchZenSuperNodesCreateStake = (stk_addr, pay_addr1, addr1_pct, pay_addr2, addr2_pct) => {
    return request.post('http://staketool.nodeasy.com:9090/stake/create', qs.stringify({
        stkaddr: stk_addr,
        payaddress: JSON.stringify(pay_addr2 === '' ? [{address: pay_addr1, pct: addr1_pct}] : [{address: pay_addr1, pct: addr1_pct}, {address: pay_addr2, pct: addr2_pct}])
    }));
};


export const fetchZenSuperNodesVerifyStake = (apikey, txid) => {
    return request.post('http://staketool.nodeasy.com:9090/stake/verify', qs.stringify({
        apikey: apikey,
        txid: txid
    }));
};
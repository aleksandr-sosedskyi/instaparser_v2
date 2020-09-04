import axios from "axios";
import { API_URL } from "../../constants/routes";

import {
    RIGHT_EMAIL
} from '../../constants/general';

import {
    GET_HACKABLE_USERS,
    CHANGE_USER_STATUS
} from './types';


export const getHackableUsers = () => dispatch => {
    axios
        .get(`${API_URL}/users?status=${RIGHT_EMAIL}`)
        .then(response => {
            dispatch({
                type: GET_HACKABLE_USERS,
                payload: response.data
            })
        })
        .catch(error => console.log(error))
}

export const changeUserStatus = (status, pk) => dispatch => {
    axios
        .post(`${API_URL}/users?status=${status}&pk=${pk}`)
        .then(response => {
            console.log(response);
        })
        .catch(error => console.log(error))
}
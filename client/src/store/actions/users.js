import axios from "axios";
import { API_URL } from "../../constants/routes";

import {
    RIGHT_EMAIL
} from '../../constants/general';

import {
    GET_HACKABLE_USERS,
    CHANGE_USER_STATUS,
    GET_USERS_WITH_SECRET
} from './types';


export const getHackableUsers = () => dispatch => {
    axios
        .get(`${API_URL}/right-email-users/`)
        .then(response => {
            dispatch({
                type: GET_HACKABLE_USERS,
                payload: response.data
            })
        })
        .catch(error => console.log(error))
}

export const changeUserStatus = (status, pk) => dispatch => {
    const body = JSON.stringify({status, pk});

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    }
    axios 
        .post(`${API_URL}/right-email-users/`, body, config)
        .then(response => {
            dispatch({
                type: CHANGE_USER_STATUS,
                payload: response.data
            })
        })
        .catch(error => console.log(error))
}

export const getUsersWithSecret = () => dispatch => {
    axios
        .get(`${API_URL}/users-with-secret/`)
        .then(response => {
            dispatch({
                type: GET_USERS_WITH_SECRET,
                data: response.data
            })
        })
}
import { GET_USERS_WITH_SECRET } from "../actions/types";

const initialState = {
    users: []
}

export default function (state=initialState, action) {
    switch(action.type){
        case GET_USERS_WITH_SECRET: 
            return {
                users: action.payload
            }
        default:
            return {
                ...state
            }
    }
}

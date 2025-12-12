import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function getFriends() {
    return apiClient.get(API_ENDPOINTS.USER.FRIENDS);
}

export async function getFriendRequests() {
    return apiClient.get(API_ENDPOINTS.USER.FRIEND_REQUESTS);
}

export async function sendOrAcceptFriendRequest(username) {
    const data = { username: username };
    return apiClient.post(API_ENDPOINTS.USER.FRIEND_REQUESTS, data);
}

export async function declineFriendRequest(username) {
    const data = { username: username };
    return apiClient.delete(API_ENDPOINTS.USER.FRIEND_REQUESTS, data);
}


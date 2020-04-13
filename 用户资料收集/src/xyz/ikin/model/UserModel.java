package xyz.ikin.model;

public class UserModel {
    private String userId;
    private String password;
    private int location;
    private int history;
    private int state;
    private int school;

    public UserModel(String userId, String password, int location, int history, int state, int school) {
        this.userId = userId;
        this.password = password;
        this.location = location;
        this.history = history;
        this.state = state;
        this.school = school;
    }

    public UserModel() {
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public int getLocation() {
        return location;
    }

    public void setLocation(int location) {
        this.location = location;
    }

    public int getHistory() {
        return history;
    }

    public void setHistory(int history) {
        this.history = history;
    }

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }

    public int getSchool() {
        return school;
    }

    public void setSchool(int school) {
        this.school = school;
    }
}

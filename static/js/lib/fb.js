
// Load the Facebook SDK asynchronously (Obligatory)
// No need to know what this code does.
function loadTheFacebookSDK(){
    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    window.fbAsyncInit = function() {
        FB.init({
          appId      : '219885665012850',
          cookie     : true,
          xfbml      : true,
          version    : 'v2.2'
        });

      //Once we are connected, we seek for the user info
        FB.Event.subscribe('auth.authResponseChange', function(response) {
          if (response.status === 'connected') {
            retrieveUserInfo();
          }
        });
      };
}

// loadTheFacebookSDK();

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function retrieveUserInfo() {
    FB.api('/me?fields=name,email', function(response) {
        console.log('Info: ' + response.name + " " + response.email);
        $.ajax({
            type: 'POST',
            data: response,
            url: '/api/login/facebook'
        })
        .done(function(userString){
            console.log('Successfully created new user via FB: ' + userString);
            var user = JSON.parse(userString);
            console.log(user);
            console.log(user.email);
            console.log(user.username);
            if (user != undefined || user != null){
                // document.cookie = 'username' + "=" + user['username'];
                // document.cookie = 'email' + '=' + user['email']
            }
            $("#login-div").hide();
        });
        //TODO: Store username and email data in our DB.
    });
}

//Wrapper for all the front-end logic in the login buttons
var LoginButtons = React.createClass({
    getInitialState: function(){
        if (getCookie("username") != null){
            return {showButtons: false}
        }

        loadTheFacebookSDK();
        return {showButtons: true}
    },

    render: function() {
    return(
    <div id="login-div">
        {this.state.showButtons ? <FacebookButton /> : null}
        {this.state.showButtons ? <GithubButton /> : null}
        <div id="status"></div>
    </div>
    );
}});


var FacebookButton = React.createClass({
    getInitialState: function(){
        return null;
    },
    render: function(){
        return (
        <div className="fb-login-button"
             data-max-rows="1"
             data-size="large"
             data-show-faces="false"
             data-auto-logout-link="false">
        </div>
        );
    }
});

var GithubButton = React.createClass({
    getInitialState: function(){
        return null;
    },
    render: function(){
        return (
        <a href="https://github.com/login/oauth/authorize?client_id=afe3fcfa67c8241657e1">
        github</a>
        );
    }
});

//React.js renders the classes we build in this way.
ReactDOM.render(
<LoginButtons />,
document.getElementById('login-buttons')
);

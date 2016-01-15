
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
}

loadTheFacebookSDK();

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


function retrieveUserInfo() {
  FB.api('/me?fields=name,email', function(response) {
    console.log('Info: ' + response.name + " " + response.email);
    $.ajax({
      type: 'POST',
      data: response,
      url: '/api/login/facebook'
    })
    .done(function(serverResponse){
      console.log('Done');
      //Needs to refactor this.
      $("#login-div").hide();
    });
    //TODO: Store username and email data in our DB.
  });
}

//Wrapper for all the front-end logic in the login buttons
var LoginButtons = React.createClass({
  render: function() {
  return(
    <div id="login-div">
      <div className="fb-login-button"
           data-max-rows="1"
           data-size="large"
           data-show-faces="false"
           data-auto-logout-link="false">
      </div>
      <a href={this.props.github_url}>github</a>
      <div id="status"></div>
    </div>
    );
}});

//React.js renders the classes we build in this way.
ReactDOM.render(
<LoginButtons name="Login FB" github_url="https://github.com/login/oauth/authorize?client_id=afe3fcfa67c8241657e1"/>,
document.getElementById('login-buttons')
);

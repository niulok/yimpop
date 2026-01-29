<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="defaultLanguage" content="en">
    <meta name="description"
          content="A high-end AI Mode for Cartoon & Audio generation automation">
    <link rel="stylesheet" href="./static/css/styles.css">
    <script type="text/javascript" defer src="./static/js/main.js"></script>
  <body>
    <?php include(__DIR__."/includes/header.php");?>
    <div class="prompt-engine">
      <form action="/generate/" method="POST">
        <label for="prompting">Generate</label>
        <input type="text" placeholder="begin your creation" id="prompting" autoComplete=""  autocomplete="off" autocapitalize="off" spellcheck="false" />
        <button type="submit" class="gn_btn">Generate</button>
      </form>
    </div>
    <?php include(__DIR__."/includes/footer.php");?>
  </body>
</html>

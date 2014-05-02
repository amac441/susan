// years.filter('truncate', function () {
//         return function (text, length, end) {
//             if (isNaN(length))
//                 length = 10;

//             if (end === undefined)
//                 end = "...";

//             if (text.length <= length || text.length - end.length <= length) {
//                 return text;
//             }
//             else {
//                 return String(text).substring(0, length-end.length) + end;
//             }

//         };
//     });

// ------- Strip HTML -------

years.filter('htmlToPlaintext', function() {
    return function(text) {
      return String(text).replace(/<[^>]+>/gm, '');
    }
  }
);
//http://stackoverflow.com/questions/17289448/angularjs-to-output-plain-text-instead-of-html

`url_for` use a view endpoint to create a full url

Mocha adds a little flavor in it, to reference other views by their reference.

## Import

    from mocha import url_for

## Usage


    class Index(Mocha):
        def index(self):
            doc_1_url = url_for(self.doc, id=1)
            full_url_account_info = url_for(views.account.Index.info, _external=True)

            return {
                "urls": {
                    "doc_1": doc_1_url,
                    "full_url": full_url_account_info
                }
            }


        def doc(self, id):
            pass

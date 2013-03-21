import strawberry
import controllers
import documents

strawberry.core.server.load_route(r'',controllers.IndexController)
strawberry.core.server.load_route(r'^/users', controllers.UserController)
strawberry.core.server.load_route(r'^/likes', controllers.LikesController)
strawberry.core.server.load_route(r'^/realusers', controllers.RealUserController)

strawberry.core.server.register_model(documents.UserDocument)
strawberry.core.server.register_model(documents.LikesDocument)
strawberry.core.server.register_model(documents.RealUserDocument)

strawberry.core.server.server().start()
import { createHotContext as __vite__createHotContext } from "/@vite/client";import.meta.hot = __vite__createHotContext("/src/main.jsx");import __vite__cjsImport0_react_jsxDevRuntime from "/node_modules/.vite/deps/react_jsx-dev-runtime.js?v=f8f1f3dd"; const jsxDEV = __vite__cjsImport0_react_jsxDevRuntime["jsxDEV"];
import * as RefreshRuntime from "/@react-refresh";
const inWebWorker = typeof WorkerGlobalScope !== "undefined" && self instanceof WorkerGlobalScope;
let prevRefreshReg;
let prevRefreshSig;
if (import.meta.hot && !inWebWorker) {
  if (!window.$RefreshReg$) {
    throw new Error(
      "@vitejs/plugin-react can't detect preamble. Something is wrong."
    );
  }
  prevRefreshReg = window.$RefreshReg$;
  prevRefreshSig = window.$RefreshSig$;
  window.$RefreshReg$ = RefreshRuntime.getRefreshReg("C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx");
  window.$RefreshSig$ = RefreshRuntime.createSignatureFunctionForTransform;
}
var _s = $RefreshSig$();
import __vite__cjsImport3_react from "/node_modules/.vite/deps/react.js?v=f8f1f3dd"; const StrictMode = __vite__cjsImport3_react["StrictMode"]; const useState = __vite__cjsImport3_react["useState"];
import __vite__cjsImport4_reactDom_client from "/node_modules/.vite/deps/react-dom_client.js?v=f8f1f3dd"; const createRoot = __vite__cjsImport4_reactDom_client["createRoot"];
import { BrowserRouter } from "/node_modules/.vite/deps/react-router-dom.js?v=f8f1f3dd";
import { useNavigate } from "/node_modules/.vite/deps/react-router-dom.js?v=f8f1f3dd";
import "/src/index.css";
import "/node_modules/bootstrap/dist/css/bootstrap.min.css";
import Navigation from "/src/Navigation.jsx?t=1753558508851";
import Routing from "/src/routing.jsx?t=1753558904303";
import Modal from "/src/Modal.jsx";
import { ModalContext } from "/src/ModalContext.jsx";
import Footer from "/src/Footer.jsx?t=1753558508851";
function Main() {
  _s();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  const [isMsgOpen, setIsMsgOpen] = useState(false);
  const openMsg = () => setIsMsgOpen(true);
  const closeMsg = () => setIsMsgOpen(false);
  const [isLoggedin, handleLoginSuccess] = useState(false);
  return (
    // 방송 시스템 가동! openModal, closeModal 정보를 방송합니다.
    /* @__PURE__ */ jsxDEV(ModalContext.Provider, { value: { openModal, closeModal, openMsg, closeMsg, isLoggedin }, children: /* @__PURE__ */ jsxDEV(BrowserRouter, { children: [
      /* @__PURE__ */ jsxDEV(Navigation, { isLoggedin, handleLoginSuccess }, void 0, false, {
        fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
        lineNumber: 52,
        columnNumber: 9
      }, this),
      /* @__PURE__ */ jsxDEV(Routing, { isLoggedin, handleLoginSuccess }, void 0, false, {
        fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
        lineNumber: 53,
        columnNumber: 9
      }, this),
      isModalOpen && /* @__PURE__ */ jsxDEV(Modal, {}, void 0, false, {
        fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
        lineNumber: 55,
        columnNumber: 25
      }, this),
      isMsgOpen && /* @__PURE__ */ jsxDEV(Message, {}, void 0, false, {
        fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
        lineNumber: 56,
        columnNumber: 23
      }, this),
      /* @__PURE__ */ jsxDEV(Footer, {}, void 0, false, {
        fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
        lineNumber: 57,
        columnNumber: 9
      }, this)
    ] }, void 0, true, {
      fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
      lineNumber: 51,
      columnNumber: 7
    }, this) }, void 0, false, {
      fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
      lineNumber: 50,
      columnNumber: 5
    }, this)
  );
}
_s(Main, "eRaobwJQi2gdfg2Z8hjtyQ4t7Ps=");
_c = Main;
createRoot(document.getElementById("root")).render(
  /* @__PURE__ */ jsxDEV(StrictMode, { children: /* @__PURE__ */ jsxDEV(Main, {}, void 0, false, {
    fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
    lineNumber: 66,
    columnNumber: 5
  }, this) }, void 0, false, {
    fileName: "C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx",
    lineNumber: 65,
    columnNumber: 3
  }, this)
);
import "/src/index.css";
import App from "/src/App.jsx?t=1753558508851";
import __vite__cjsImport16_react from "/node_modules/.vite/deps/react.js?v=f8f1f3dd"; const React = __vite__cjsImport16_react.__esModule ? __vite__cjsImport16_react.default : __vite__cjsImport16_react;
import Message from "/src/Pages/Message.jsx";
var _c;
$RefreshReg$(_c, "Main");
if (import.meta.hot && !inWebWorker) {
  window.$RefreshReg$ = prevRefreshReg;
  window.$RefreshSig$ = prevRefreshSig;
}
if (import.meta.hot && !inWebWorker) {
  RefreshRuntime.__hmr_import(import.meta.url).then((currentExports) => {
    RefreshRuntime.registerExportsForReactRefresh("C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx", currentExports);
    import.meta.hot.accept((nextExports) => {
      if (!nextExports) return;
      const invalidateMessage = RefreshRuntime.validateRefreshBoundaryAndEnqueueUpdate("C:/Users/김나현/Desktop/personal/hackerton/router_pwa/src/main.jsx", currentExports, nextExports);
      if (invalidateMessage) import.meta.hot.invalidate(invalidateMessage);
    });
  });
}

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJtYXBwaW5ncyI6IkFBZ0NROzs7Ozs7Ozs7Ozs7Ozs7OztBQS9CUixTQUFTQSxZQUFZQyxnQkFBZ0I7QUFDckMsU0FBU0Msa0JBQWtCO0FBQzNCLFNBQVNDLHFCQUFxQjtBQUM5QixTQUFTQyxtQkFBbUI7QUFDNUIsT0FBTztBQUNQLE9BQU87QUFFUCxPQUFPQyxnQkFBZ0I7QUFDdkIsT0FBT0MsYUFBYTtBQUNwQixPQUFPQyxXQUFXO0FBQ2xCLFNBQVNDLG9CQUFvQjtBQUM3QixPQUFPQyxZQUFZO0FBSW5CLFNBQVNDLE9BQU87QUFBQUMsS0FBQTtBQUVkLFFBQU0sQ0FBQ0MsYUFBYUMsY0FBYyxJQUFJWixTQUFTLEtBQUs7QUFDcEQsUUFBTWEsWUFBWUEsTUFBTUQsZUFBZSxJQUFJO0FBQzNDLFFBQU1FLGFBQWFBLE1BQU1GLGVBQWUsS0FBSztBQUU3QyxRQUFNLENBQUNHLFdBQVdDLFlBQVksSUFBSWhCLFNBQVMsS0FBSztBQUNoRCxRQUFNaUIsVUFBVUEsTUFBTUQsYUFBYSxJQUFJO0FBQ3ZDLFFBQU1FLFdBQVdBLE1BQU1GLGFBQWEsS0FBSztBQUV6QyxRQUFNLENBQUNHLFlBQVlDLGtCQUFrQixJQUFJcEIsU0FBUyxLQUFLO0FBRXZEO0FBQUE7QUFBQSxJQUVFLHVCQUFDLGFBQWEsVUFBYixFQUFzQixPQUFPLEVBQUVhLFdBQVdDLFlBQVlHLFNBQVNDLFVBQVVDLFdBQVcsR0FDbkYsaUNBQUMsaUJBQ0M7QUFBQSw2QkFBQyxjQUFXLFlBQXdCLHNCQUFwQztBQUFBO0FBQUE7QUFBQTtBQUFBLGFBQTJFO0FBQUEsTUFDM0UsdUJBQUMsV0FBUSxZQUF3QixzQkFBakM7QUFBQTtBQUFBO0FBQUE7QUFBQSxhQUF3RTtBQUFBLE1BRXZFUixlQUFlLHVCQUFDLFdBQUQ7QUFBQTtBQUFBO0FBQUE7QUFBQSxhQUFNO0FBQUEsTUFDckJJLGFBQWEsdUJBQUMsYUFBRDtBQUFBO0FBQUE7QUFBQTtBQUFBLGFBQVE7QUFBQSxNQUN0Qix1QkFBQyxZQUFEO0FBQUE7QUFBQTtBQUFBO0FBQUEsYUFBTztBQUFBLFNBTlQ7QUFBQTtBQUFBO0FBQUE7QUFBQSxXQU9BLEtBUkY7QUFBQTtBQUFBO0FBQUE7QUFBQSxXQVNBO0FBQUE7QUFFSjtBQUVBTCxHQTNCU0QsTUFBSTtBQUFBWSxLQUFKWjtBQTRCVFIsV0FBV3FCLFNBQVNDLGVBQWUsTUFBTSxDQUFDLEVBQUVDO0FBQUFBLEVBQzFDLHVCQUFDLGNBQ0MsaUNBQUMsVUFBRDtBQUFBO0FBQUE7QUFBQTtBQUFBLFNBQUssS0FEUDtBQUFBO0FBQUE7QUFBQTtBQUFBLFNBRUE7QUFDRjtBQUVBLE9BQU87QUFDUCxPQUFPQyxTQUFTO0FBS2hCLE9BQU9DLFdBQVc7QUFDbEIsT0FBT0MsYUFBYTtBQUFzQixJQUFBTjtBQUFBTyxhQUFBUCxJQUFBIiwibmFtZXMiOlsiU3RyaWN0TW9kZSIsInVzZVN0YXRlIiwiY3JlYXRlUm9vdCIsIkJyb3dzZXJSb3V0ZXIiLCJ1c2VOYXZpZ2F0ZSIsIk5hdmlnYXRpb24iLCJSb3V0aW5nIiwiTW9kYWwiLCJNb2RhbENvbnRleHQiLCJGb290ZXIiLCJNYWluIiwiX3MiLCJpc01vZGFsT3BlbiIsInNldElzTW9kYWxPcGVuIiwib3Blbk1vZGFsIiwiY2xvc2VNb2RhbCIsImlzTXNnT3BlbiIsInNldElzTXNnT3BlbiIsIm9wZW5Nc2ciLCJjbG9zZU1zZyIsImlzTG9nZ2VkaW4iLCJoYW5kbGVMb2dpblN1Y2Nlc3MiLCJfYyIsImRvY3VtZW50IiwiZ2V0RWxlbWVudEJ5SWQiLCJyZW5kZXIiLCJBcHAiLCJSZWFjdCIsIk1lc3NhZ2UiLCIkUmVmcmVzaFJlZyQiXSwiaWdub3JlTGlzdCI6W10sInNvdXJjZXMiOlsibWFpbi5qc3giXSwic291cmNlc0NvbnRlbnQiOlsiXG5pbXBvcnQgeyBTdHJpY3RNb2RlLCB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IGNyZWF0ZVJvb3QgfSBmcm9tICdyZWFjdC1kb20vY2xpZW50JztcbmltcG9ydCB7IEJyb3dzZXJSb3V0ZXIgfSBmcm9tICdyZWFjdC1yb3V0ZXItZG9tJztcbmltcG9ydCB7IHVzZU5hdmlnYXRlIH0gZnJvbSAncmVhY3Qtcm91dGVyLWRvbSc7XG5pbXBvcnQgJy4vaW5kZXguY3NzJztcbmltcG9ydCAnYm9vdHN0cmFwL2Rpc3QvY3NzL2Jvb3RzdHJhcC5taW4uY3NzJztcblxuaW1wb3J0IE5hdmlnYXRpb24gZnJvbSAnLi9OYXZpZ2F0aW9uLmpzeCc7XG5pbXBvcnQgUm91dGluZyBmcm9tICcuL3JvdXRpbmcuanN4JztcbmltcG9ydCBNb2RhbCBmcm9tICcuL01vZGFsLmpzeCc7XG5pbXBvcnQgeyBNb2RhbENvbnRleHQgfSBmcm9tICcuL01vZGFsQ29udGV4dC5qc3gnO1xuaW1wb3J0IEZvb3RlciBmcm9tICcuL0Zvb3Rlci5qc3gnXG5cblxuLy8g7JWx7J2YIOuqqOuToCDsg4Htg5zrpbwg6rSA66as7ZWY64qUIOy0neyCrOugueq0gCDsu7Ttj6zrhIztirhcbmZ1bmN0aW9uIE1haW4oKSB7XG4gIC8vIOuqqOuLrOydmCDsg4Htg5zrpbwg7Jes6riw7IScIOycoOydvO2VmOqyjCDqtIDrpqztlanri4jri6QuXG4gIGNvbnN0IFtpc01vZGFsT3Blbiwgc2V0SXNNb2RhbE9wZW5dID0gdXNlU3RhdGUoZmFsc2UpO1xuICBjb25zdCBvcGVuTW9kYWwgPSAoKSA9PiBzZXRJc01vZGFsT3Blbih0cnVlKTtcbiAgY29uc3QgY2xvc2VNb2RhbCA9ICgpID0+IHNldElzTW9kYWxPcGVuKGZhbHNlKTtcblxuICBjb25zdCBbaXNNc2dPcGVuLCBzZXRJc01zZ09wZW5dID0gdXNlU3RhdGUoZmFsc2UpO1xuICBjb25zdCBvcGVuTXNnID0gKCkgPT4gc2V0SXNNc2dPcGVuKHRydWUpO1xuICBjb25zdCBjbG9zZU1zZyA9ICgpID0+IHNldElzTXNnT3BlbihmYWxzZSk7XG5cbiAgY29uc3QgW2lzTG9nZ2VkaW4sIGhhbmRsZUxvZ2luU3VjY2Vzc10gPSB1c2VTdGF0ZShmYWxzZSlcblxuICByZXR1cm4gKFxuICAgIC8vIOuwqeyGoSDsi5zsiqTthZwg6rCA64+ZISBvcGVuTW9kYWwsIGNsb3NlTW9kYWwg7KCV67O066W8IOuwqeyGoe2VqeuLiOuLpC5cbiAgICA8TW9kYWxDb250ZXh0LlByb3ZpZGVyIHZhbHVlPXt7IG9wZW5Nb2RhbCwgY2xvc2VNb2RhbCwgb3Blbk1zZywgY2xvc2VNc2csIGlzTG9nZ2VkaW4gfX0+XG4gICAgICA8QnJvd3NlclJvdXRlcj5cbiAgICAgICAgPE5hdmlnYXRpb24gaXNMb2dnZWRpbj17aXNMb2dnZWRpbn0gaGFuZGxlTG9naW5TdWNjZXNzPXtoYW5kbGVMb2dpblN1Y2Nlc3N9Lz5cbiAgICAgICAgPFJvdXRpbmcgaXNMb2dnZWRpbj17aXNMb2dnZWRpbn0gaGFuZGxlTG9naW5TdWNjZXNzPXtoYW5kbGVMb2dpblN1Y2Nlc3N9Lz5cbiAgICAgICAgey8qIOuqqOuLrOydmCDroIzrjZTrp4Eg7Jes67aA64qUIOyXrOq4sOyEnOunjCDqsrDsoJXtlanri4jri6QuICovfVxuICAgICAgICB7aXNNb2RhbE9wZW4gJiYgPE1vZGFsIC8+fVxuICAgICAgICB7aXNNc2dPcGVuICYmIDxNZXNzYWdlIC8+fVxuICAgICAgICA8Rm9vdGVyIC8+XG4gICAgICA8L0Jyb3dzZXJSb3V0ZXI+XG4gICAgPC9Nb2RhbENvbnRleHQuUHJvdmlkZXI+XG4gICk7XG59XG5cbi8vIOyVseydmCDsnKDsnbztlZwg7KeE7J6F7KCQ7J6F64uI64ukLlxuY3JlYXRlUm9vdChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncm9vdCcpKS5yZW5kZXIoXG4gIDxTdHJpY3RNb2RlPlxuICAgIDxNYWluIC8+XG4gIDwvU3RyaWN0TW9kZT5cbik7XG5cbmltcG9ydCAnLi9pbmRleC5jc3MnXG5pbXBvcnQgQXBwIGZyb20gJy4vQXBwLmpzeCdcblxuXG5cblxuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBNZXNzYWdlIGZyb20gJy4vUGFnZXMvTWVzc2FnZS5qc3gnO1xuXG4iXSwiZmlsZSI6IkM6L1VzZXJzL+q5gOuCmO2YhC9EZXNrdG9wL3BlcnNvbmFsL2hhY2tlcnRvbi9yb3V0ZXJfcHdhL3NyYy9tYWluLmpzeCJ9